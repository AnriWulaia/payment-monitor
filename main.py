from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection, init_db

app = FastAPI()

init_db()


class Payment(BaseModel):
    amount: float
    status: str
    merchant: str

@app.get("/payments")
def get_payments():
    conn = get_connection()
    payments = conn.execute("SELECT * FROM payments").fetchall()
    conn.close()
    return [dict(p) for p in payments]

@app.get("/payments/stats")
def get_stats():
    conn = get_connection()
    result = conn.execute("""
        SELECT 
            COUNT(*) as total,
            AVG(amount) as average_amount,
            SUM(amount) as total_volume,
            SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate
        FROM payments
    """).fetchone()
    conn.close()
    return dict(result)

@app.get("/payments/suspicious")
def get_suspicious():
    conn = get_connection()
    payments = conn.execute(
        "SELECT * FROM payments WHERE amount > 10000"
    ).fetchall()
    conn.close()
    return [dict(p) for p in payments]

@app.get("/payments/{id}")
def get_payment(id: int):
    conn = get_connection()
    payment = conn.execute(
        "SELECT * FROM payments WHERE id = ?", (id,)
    ).fetchone()
    conn.close()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return dict(payment)

@app.post("/payments")
def add_payment(payment: Payment):
    conn = get_connection()
    conn.execute(
        "INSERT INTO payments (amount, status, merchant) VALUES (?, ?, ?)",
        (payment.amount, payment.status, payment.merchant)
    )
    conn.commit()
    conn.close()
    return {"message": "Payment added successfully"}