import json
from flask import Flask, request, jsonify
from .calculator import FinancialCalculator

app = Flask("__name__")

@app.route('/', methods=['POST'])
def main():
    if not request.form:
        return { "msg":"got nothing!"}
    post_body = request.form.to_dict()
    calculator = FinancialCalculator(**post_body)
    response = {
        "decimal_current_yield": str(calculator.decimal_current_yield),
        "decimal_future_yield": str(calculator.decimal_future_yield),
        "monthly_yield_current": str(calculator.monthly_yield_current),
        "monthly_yield_goal": str(calculator.monthly_yield_goal),
        "contribution_years": str(calculator.contribution_years),
        "contribution_months": str(calculator.contribution_months),
        "consumption_months": str(calculator.consumption_months),
        "consumable_patrimony_value": str(calculator.consumable_patrimony_value),
        "infinity_patrimony_value": str(calculator.infinity_patrimony_value),
    }
    return jsonify(response), 201


if __name__ == "__main__":
    app.run()