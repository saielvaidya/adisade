from database import get_expenses
from expenses import calculate_total_monthly


def calculate_category_breakdown():
    expenses = get_expenses()

    category_totals = {}

    for expense in expenses:
        category = expense["category"]
        monthly_cost = expense["monthly_cost"]

        if category in category_totals:
            category_totals[category] += monthly_cost
        else:
            category_totals[category] = monthly_cost

    return category_totals


def calculate_category_percentages():
    category_totals = calculate_category_breakdown()

    total = sum(category_totals.values())

    percentages = {}

    if total == 0:
        return percentages

    for category, amount in category_totals.items():
        percentages[category] = (amount / total) * 100

    return percentages


def build_financial_profile():
    expenses = get_expenses()

    monthly_total = calculate_total_monthly()
    yearly_total = monthly_total * 12

    category_totals = calculate_category_breakdown()
    category_percentages = calculate_category_percentages()

    largest_expense = None

    if expenses:
        largest_expense = max(
            expenses,
            key=lambda expense: expense["monthly_cost"]
        )

    financial_profile = {
        "monthly_total": monthly_total,
        "yearly_total": yearly_total,
        "active_expenses": len(expenses),
        "category_totals": category_totals,
        "category_percentages": category_percentages,
        "largest_expense": largest_expense,
        "expenses": expenses
    }

    return financial_profile

