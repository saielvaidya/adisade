from flask import Flask, render_template, request, jsonify

from analysis import (
    calculate_category_breakdown,
    calculate_category_percentages,
    build_financial_profile
)

from expenses import (
    add_expense,
    calculate_monthly,
    calculate_total_monthly
)

from database import (
    get_expenses,
    delete_expense,
    update_expense
)

from ai import generate_recommendations


app = Flask(__name__)


def get_app_data():
    expenses = get_expenses()

    category_totals = calculate_category_breakdown()
    category_percentages = calculate_category_percentages()

    total_monthly = calculate_total_monthly()
    total_yearly = total_monthly * 12
    active_expenses = len(expenses)

    largest_expense = None

    if expenses:
        largest_expense = max(
            expenses,
            key=lambda expense: expense["monthly_cost"]
        )

    return {
        "expenses": expenses,
        "total_monthly": total_monthly,
        "total_yearly": total_yearly,
        "active_expenses": active_expenses,
        "largest_expense": largest_expense,
        "category_totals": category_totals,
        "category_percentages": category_percentages
    }


@app.route("/")
def home():
    data = get_app_data()

    return render_template(
        "index.html",
        **data
    )


@app.route("/add-expense", methods=["POST"])
def add_expense_route():
    data = request.get_json()

    name = data["name"]
    amount = float(data["amount"])
    frequency = data["frequency"]
    category = data["category"]

    add_expense(
        name,
        amount,
        frequency,
        category
    )

    return jsonify(get_app_data())


@app.route("/delete-expense/<int:expense_id>", methods=["DELETE"])
def delete_expense_route(expense_id):
    delete_expense(expense_id)

    return jsonify(get_app_data())


@app.route("/update-expense/<int:expense_id>", methods=["PUT"])
def update_expense_route(expense_id):
    data = request.get_json()

    name = data["name"]
    amount = float(data["amount"])
    frequency = data["frequency"]
    category = data["category"]

    monthly_cost = calculate_monthly(
        amount,
        frequency
    )

    update_expense(
        expense_id,
        name,
        amount,
        frequency,
        category,
        monthly_cost
    )

    return jsonify(get_app_data())


@app.route("/ai-analysis", methods=["POST"])
def ai_analysis_route():
    financial_profile = build_financial_profile()

    recommendation = generate_recommendations(
        financial_profile
    )

    return jsonify({
        "recommendation": recommendation
    })


if __name__ == "__main__":
    app.run(debug=True, port=5004)