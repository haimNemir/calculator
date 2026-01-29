from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/health")
def health():
    return {"status": "ok"}

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

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
