import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row


load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection(row_factory=None):
    return psycopg.connect(
        DATABASE_URL,
        row_factory=row_factory
    )


def create_users_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    connection.commit()

    cursor.close()
    connection.close()


def create_expenses_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            frequency TEXT NOT NULL,
            category TEXT NOT NULL,
            monthly_cost REAL NOT NULL
        )
    """)

    connection.commit()

    cursor.close()
    connection.close()


def add_user_id_to_expenses():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        ALTER TABLE expenses
        ADD COLUMN IF NOT EXISTS user_id INTEGER
        REFERENCES users(id)
        ON DELETE CASCADE
    """)

    connection.commit()

    cursor.close()
    connection.close()


def create_user(
    email,
    password_hash
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users (
            email,
            password_hash
        )
        VALUES (%s, %s)
    """, (
        email,
        password_hash
    ))

    connection.commit()

    cursor.close()
    connection.close()


def get_user_by_email(email):
    connection = get_connection(
        row_factory=dict_row
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email = %s
    """, (
        email,
    ))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user


def get_user_by_id(user_id):
    connection = get_connection(
        row_factory=dict_row
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE id = %s
    """, (
        user_id,
    ))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user


def save_expenses(
    user_id,
    name,
    amount,
    frequency,
    category,
    monthly_cost
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses (
            user_id,
            name,
            amount,
            frequency,
            category,
            monthly_cost
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        name,
        amount,
        frequency,
        category,
        monthly_cost
    ))

    connection.commit()

    cursor.close()
    connection.close()


def get_expenses(user_id):
    connection = get_connection(
        row_factory=dict_row
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM expenses
        WHERE user_id = %s
        ORDER BY id
    """, (
        user_id,
    ))

    expenses = cursor.fetchall()

    cursor.close()
    connection.close()

    return expenses


def delete_expense(
    expense_id,
    user_id
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = %s
        AND user_id = %s
    """, (
        expense_id,
        user_id
    ))

    connection.commit()

    cursor.close()
    connection.close()


def update_expense(
    expense_id,
    user_id,
    name,
    amount,
    frequency,
    category,
    monthly_cost
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses
        SET name = %s,
            amount = %s,
            frequency = %s,
            category = %s,
            monthly_cost = %s
        WHERE id = %s
        AND user_id = %s
    """, (
        name,
        amount,
        frequency,
        category,
        monthly_cost,
        expense_id,
        user_id
    ))

    connection.commit()

    cursor.close()
    connection.close()


create_users_table()
create_expenses_table()
add_user_id_to_expenses()