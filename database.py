import sqlite3
from werkzeug.security import generate_password_hash


DATABASE = "database.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            brand TEXT,
            description TEXT,
            price REAL,
            rating REAL
        )
    """)

    # User activity table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            activity_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
        )
    """)

    connection.commit()

    connection.close()


def add_user(name, email, password):

    connection = get_connection()

    cursor = connection.cursor()

    hashed_password = generate_password_hash(password)

    try:

        cursor.execute("""
            INSERT INTO users
            (name, email, password)
            VALUES (?, ?, ?)
        """, (name, email, hashed_password))

        connection.commit()

        user_id = cursor.lastrowid

        connection.close()

        return user_id

    except sqlite3.IntegrityError:

        connection.close()

        return None


def get_user_by_email(email):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    connection.close()

    return user


def add_activity(user_id, product_id, activity_type):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO user_activity
        (user_id, product_id, activity_type)
        VALUES (?, ?, ?)
    """, (user_id, product_id, activity_type))

    connection.commit()

    connection.close()


def get_recently_viewed(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT product_id
        FROM user_activity
        WHERE user_id = ?
        AND activity_type = 'view'
        ORDER BY created_at DESC
        LIMIT 5
    """, (user_id,))

    products = cursor.fetchall()

    connection.close()

    return products