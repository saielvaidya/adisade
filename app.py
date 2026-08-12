import os

from flask import Flask, render_template, request, jsonify
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from user import User

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
    update_expense,
    get_user_by_id,
    get_user_by_email,
    create_user
)

from ai import generate_recommendations


app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_id(user_id)

    if user_data is None:
        return None

    return User(
        user_data["id"],
        user_data["email"]
    )


def get_app_data():
    expenses = get_expenses(
        current_user.id
    )

    total_monthly = calculate_total_monthly(
        expenses
    )

    total_yearly = total_monthly * 12

    category_totals = calculate_category_breakdown(
        expenses
    )

    category_percentages = calculate_category_percentages(
        expenses
    )

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
    if not current_user.is_authenticated:
        return render_template(
            "index.html",
            expenses=[],
            total_monthly=0,
            total_yearly=0,
            active_expenses=0,
            largest_expense=None,
            category_totals={},
            category_percentages={}
        )

    data = get_app_data()

    return render_template(
        "index.html",
        **data
    )


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    if not email:
        return jsonify({
            "error": "Email is required."
        }), 400

    if not password:
        return jsonify({
            "error": "Password is required."
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters."
        }), 400

    existing_user = get_user_by_email(
        email
    )

    if existing_user:
        return jsonify({
            "error": "An account with this email already exists."
        }), 400

    password_hash = generate_password_hash(
        password
    )

    create_user(
        email,
        password_hash
    )

    return jsonify({
        "message": "Account created successfully."
    })


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    if not email or not password:
        return jsonify({
            "error": "Email and password are required."
        }), 400

    user_data = get_user_by_email(
        email
    )

    if user_data is None:
        return jsonify({
            "error": "Invalid email or password."
        }), 401

    password_is_correct = check_password_hash(
        user_data["password_hash"],
        password
    )

    if not password_is_correct:
        return jsonify({
            "error": "Invalid email or password."
        }), 401

    user = User(
        user_data["id"],
        user_data["email"]
    )

    login_user(user)

    return jsonify({
        "message": "Logged in successfully."
    })


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()

    return jsonify({
        "message": "Logged out successfully."
    })


@app.route("/add-expense", methods=["POST"])
@login_required
def add_expense_route():
    data = request.get_json() or {}

    name = data.get(
        "name",
        ""
    ).strip()

    category = data.get(
        "category",
        ""
    ).strip()

    frequency = data.get(
        "frequency",
        ""
    ).strip()

    try:
        amount = float(
            data.get(
                "amount",
                0
            )
        )
    except (TypeError, ValueError):
        return jsonify({
            "error": "Amount must be a valid number."
        }), 400

    if not name:
        return jsonify({
            "error": "Expense name is required."
        }), 400

    if amount <= 0:
        return jsonify({
            "error": "Amount must be greater than 0."
        }), 400

    if frequency not in [
        "Weekly",
        "Monthly",
        "Yearly"
    ]:
        return jsonify({
            "error": "Invalid frequency."
        }), 400

    if not category:
        return jsonify({
            "error": "Category is required."
        }), 400

    add_expense(
        current_user.id,
        name,
        amount,
        frequency,
        category
    )

    return jsonify(
        get_app_data()
    )


@app.route(
    "/delete-expense/<int:expense_id>",
    methods=["DELETE"]
)
@login_required
def delete_expense_route(expense_id):
    delete_expense(
        expense_id,
        current_user.id
    )

    return jsonify(
        get_app_data()
    )


@app.route(
    "/update-expense/<int:expense_id>",
    methods=["PUT"]
)
@login_required
def update_expense_route(expense_id):
    data = request.get_json() or {}

    name = data.get(
        "name",
        ""
    ).strip()

    category = data.get(
        "category",
        ""
    ).strip()

    frequency = data.get(
        "frequency",
        ""
    ).strip()

    try:
        amount = float(
            data.get(
                "amount",
                0
            )
        )
    except (TypeError, ValueError):
        return jsonify({
            "error": "Amount must be a valid number."
        }), 400

    if not name:
        return jsonify({
            "error": "Expense name is required."
        }), 400

    if amount <= 0:
        return jsonify({
            "error": "Amount must be greater than 0."
        }), 400

    if frequency not in [
        "Weekly",
        "Monthly",
        "Yearly"
    ]:
        return jsonify({
            "error": "Invalid frequency."
        }), 400

    if not category:
        return jsonify({
            "error": "Category is required."
        }), 400

    monthly_cost = calculate_monthly(
        amount,
        frequency
    )

    update_expense(
        expense_id,
        current_user.id,
        name,
        amount,
        frequency,
        category,
        monthly_cost
    )

    return jsonify(
        get_app_data()
    )


@app.route("/ai-analysis", methods=["POST"])
@login_required
def ai_analysis_route():
    expenses = get_expenses(
        current_user.id
    )

    financial_profile = build_financial_profile(
        expenses
    )

    recommendation = generate_recommendations(
        financial_profile
    )

    return jsonify({
        "recommendation": recommendation
    })


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5004
    )