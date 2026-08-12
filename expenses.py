from database import save_expenses


def add_expense(
    user_id,
    name,
    amount,
    frequency,
    category
):
    monthly_cost = calculate_monthly(
        amount,
        frequency
    )

    save_expenses(
        user_id,
        name,
        amount,
        frequency,
        category,
        monthly_cost
    )


def calculate_monthly(
    amount,
    frequency
):
    if frequency.lower() == "monthly":
        return amount

    elif frequency.lower() == "yearly":
        return amount / 12

    elif frequency.lower() == "weekly":
        return (amount * 52) / 12

    else:
        return None


def calculate_total_monthly(expenses):
    total = 0

    for expense in expenses:
        total += expense["monthly_cost"]

    return total