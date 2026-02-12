from flask import Flask, request, jsonify
import os
import pymysql


app = Flask(__name__)

@app.get("/health")
def health():
    return {"status": "ok"}

def _db_config():
    return {
        "host": os.getenv("DB_HOST", "mysql"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "database": os.getenv("DB_NAME", "calculator"),
        "user": os.getenv("DB_USER", "calculator"),
        "password": os.getenv("DB_PASSWORD", ""),
    }

def get_db_connection():
    cfg = _db_config()
    return pymysql.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        connect_timeout=2,
        read_timeout=2,
        write_timeout=2,
        autocommit=False,
    )

    
@app.get("/health/db")
def health_db():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            cur.fetchone()
        return {"status": "ok", "db": "ok"}
    except Exception as e:
        return jsonify({"status": "fail", "db": "fail", "error": str(e)}), 500
    finally:
        if conn:
            conn.close()


def save_calc(a: float, b: float, op: str, result: float) -> None:
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO calc_history (a, b, op, result) VALUES (%s, %s, %s, %s)",
                (a, b, op, result),
            )
        conn.commit()
    finally:
        conn.close()

def get_history(limit: int = 20):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, a, b, op, result, created_at
                FROM calc_history
                ORDER BY id DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()
        return [
            {
                "id": r[0],
                "a": float(r[1]),
                "b": float(r[2]),
                "op": r[3],
                "result": float(r[4]),
                "created_at": str(r[5]),
            }
            for r in rows
        ]
    finally:
        conn.close()


@app.post("/api/calc")
def calc():
    data = request.get_json(silent=True) or {}
    a = data.get("a")
    b = data.get("b")
    op = data.get("op")

    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return jsonify({"error": "a and b must be numbers"}), 400

    if op not in ["+", "-", "*", "/"]:
        return jsonify({"error": "op must be one of: +, -, *, /"}), 400

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    else:
        if b == 0:
            return jsonify({"error": "division by zero"}), 400
        result = a / b
    try:
        save_calc(a, b, op, result)
    except Exception as e:
        pass

    return jsonify({"result": result})

@app.get("/api/history")
def history():
    raw = request.args.get("limit", "20")
    try:
        limit = int(raw)
    except ValueError:
        return jsonify({"error": "limit must be an integer"}), 400

    if limit < 1:
        limit = 1
    if limit > 100:
        limit = 100

    items = get_history(limit)
    return jsonify({"items": items})





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
