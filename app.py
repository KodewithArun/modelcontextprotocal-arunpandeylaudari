from datetime import date, datetime
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from db import get_db

app = FastAPI(title="Expenses Tracker", description="Personal finance tracker")


class CategoryOut(BaseModel):
    id: int
    name: str
    type: str

class CategoryIn(BaseModel):
    name: str
    type: str

class TransactionOut(BaseModel):
    id: int
    amount: float
    description: str
    date: str
    type: str
    category_id: int
    category_name: str

class TransactionIn(BaseModel):
    amount: float
    category_id: int
    description: str = ""
    date: str = ""
    type: str = "expense"


@app.get("/api/categories", response_model=list[CategoryOut])
def list_categories(type: str = ""):
    conn = get_db()
    if type:
        rows = conn.execute(
            "SELECT id, name, type FROM categories WHERE type = ? ORDER BY name", (type,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, name, type FROM categories ORDER BY type, name"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/categories", response_model=CategoryOut)
def add_category(body: CategoryIn):
    if body.type not in ("expense", "income"):
        raise HTTPException(400, "type must be expense or income")
    conn = get_db()
    try:
        cur = conn.execute("INSERT INTO categories (name, type) VALUES (?, ?)", (body.name, body.type))
        conn.commit()
        row = conn.execute("SELECT id, name, type FROM categories WHERE id = ?", (cur.lastrowid,)).fetchone()
        conn.close()
        return dict(row)
    except Exception as e:
        conn.close()
        raise HTTPException(400, str(e))

@app.delete("/api/categories/{cat_id}")
def delete_category(cat_id: int):
    conn = get_db()
    try:
        conn.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
        conn.commit()
        conn.close()
        return {"ok": True}
    except Exception as e:
        conn.close()
        raise HTTPException(400, str(e))

@app.get("/api/transactions", response_model=list[TransactionOut])
def list_transactions(
    start_date: str = "", end_date: str = "",
    category_id: int = 0, type: str = "", limit: int = 100, offset: int = 0,
):
    query = """
        SELECT t.id, t.amount, t.description, t.date, t.type,
               c.id AS category_id, c.name AS category_name
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE 1=1
    """
    params = []
    if start_date:
        query += " AND t.date >= ?"; params.append(start_date)
    if end_date:
        query += " AND t.date <= ?"; params.append(end_date)
    if category_id:
        query += " AND t.category_id = ?"; params.append(category_id)
    if type:
        query += " AND t.type = ?"; params.append(type)
    query += " ORDER BY t.date DESC, t.id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    conn = get_db()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/transactions", response_model=TransactionOut)
def add_transaction(body: TransactionIn):
    if body.amount <= 0:
        raise HTTPException(400, "amount must be positive")
    if body.type not in ("expense", "income"):
        raise HTTPException(400, "type must be expense or income")
    tx_date = body.date or datetime.today().strftime("%Y-%m-%d")
    conn = get_db()
    try:
        cur = conn.execute(
            "INSERT INTO transactions (amount, category_id, description, date, type) VALUES (?, ?, ?, ?, ?)",
            (body.amount, body.category_id, body.description, tx_date, body.type),
        )
        conn.commit()
        row = conn.execute(
            """SELECT t.id, t.amount, t.description, t.date, t.type,
                      c.id AS category_id, c.name AS category_name
               FROM transactions t
               JOIN categories c ON t.category_id = c.id
               WHERE t.id = ?""", (cur.lastrowid,)
        ).fetchone()
        conn.close()
        return dict(row)
    except Exception as e:
        conn.close()
        raise HTTPException(400, str(e))

@app.delete("/api/transactions/{tx_id}")
def delete_transaction(tx_id: int):
    conn = get_db()
    conn.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
    conn.commit()
    conn.close()
    return {"ok": True}

@app.get("/api/summary")
def summary(start_date: str = "", end_date: str = ""):
    if not start_date and not end_date:
        today = date.today()
        start_date = today.replace(day=1).isoformat()
        end_date = today.isoformat()
    conn = get_db()
    totals = conn.execute(
        "SELECT type, COALESCE(SUM(amount), 0) AS total FROM transactions WHERE date >= ? AND date <= ? GROUP BY type",
        (start_date, end_date),
    ).fetchall()
    by_category = conn.execute(
        """SELECT t.type, c.name AS category, COALESCE(SUM(t.amount), 0) AS total
           FROM transactions t JOIN categories c ON t.category_id = c.id
           WHERE t.date >= ? AND t.date <= ?
           GROUP BY t.type, c.name ORDER BY t.type, total DESC""",
        (start_date, end_date),
    ).fetchall()
    count = conn.execute(
        "SELECT COUNT(*) FROM transactions WHERE date >= ? AND date <= ?",
        (start_date, end_date),
    ).fetchone()[0]
    conn.close()
    totals_dict = {r["type"]: r["total"] for r in totals}
    return {
        "period": f"{start_date} to {end_date}",
        "total_expenses": totals_dict.get("expense", 0.0),
        "total_income": totals_dict.get("income", 0.0),
        "net": totals_dict.get("income", 0.0) - totals_dict.get("expense", 0.0),
        "transaction_count": count,
        "by_category": [dict(r) for r in by_category],
    }
