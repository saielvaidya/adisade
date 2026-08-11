import sqlite3

DATABASE = "adisade.db"


def save_expenses(name, amount, frequency, category, monthly_cost):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (name, amount, frequency, category, monthly_cost)
        VALUES (?, ?, ?, ?, ?)
    """, (name, amount, frequency, category, monthly_cost))

    connection.commit()
    connection.close()


def create_table():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            frequency TEXT NOT NULL,
            category TEXT NOT NULL,
            monthly_cost REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def get_expenses():
    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM expenses
    """)

    rows = cursor.fetchall()

    connection.close()

    expenses = [dict(row) for row in rows]

    return expenses


def delete_expense(expense_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )
    connection.commit()
    connection.close()


def update_expense(
    expense_id,
    name,
    amount,
    frequency,
    category,
    monthly_cost
):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses
        SET name = ?,
            amount = ?,
            frequency = ?,
            category = ?,
            monthly_cost = ?
        WHERE id = ?
    """, (
        name,
        amount,
        frequency,
        category,
        monthly_cost,
        expense_id
    ))

    connection.commit()
    connection.close()

create_table()