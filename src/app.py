from flask import Flask, request, jsonify
from .calculator import FinancialCalculator

app = Flask("__name__")

@app.route('/calculator', methods=['POST'])
def calculator():
    if not request.json:
        return { "msg":"got nothing!"}
    data = {
        "msg1": request.json['arg1'],
        "msg2": request.json['arg2']
    }
    return jsonify(data), 201

@app.route("/")
def home():
    data = {
        "msg": "Flas is online"
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run()