import os
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL is not set")

    return psycopg2.connect(DATABASE_URL)


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
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
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            activity_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
        )
    """)

    connection.commit()

    cursor.close()
    connection.close()


def add_user(name, email, password):

    connection = get_connection()
    cursor = connection.cursor()

    hashed_password = generate_password_hash(password)

    try:

        cursor.execute("""
            INSERT INTO users
            (name, email, password)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (name, email, hashed_password))

        user_id = cursor.fetchone()[0]

        connection.commit()

        cursor.close()
        connection.close()

        return user_id

    except psycopg2.IntegrityError:

        connection.rollback()

        cursor.close()
        connection.close()

        return None


def get_user_by_email(email):

    connection = get_connection()

    cursor = connection.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email = %s
    """, (email,))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user


def add_activity(
    user_id,
    product_id,
    activity_type
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO user_activity
        (user_id, product_id, activity_type)
        VALUES (%s, %s, %s)
    """, (
        user_id,
        product_id,
        activity_type
    ))

    connection.commit()

    cursor.close()
    connection.close()


def get_recently_viewed(user_id):

    connection = get_connection()

    cursor = connection.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute("""
        SELECT product_id, MAX(created_at) AS last_viewed
        FROM user_activity
        WHERE user_id = %s
        AND activity_type = 'view'
        GROUP BY product_id
        ORDER BY last_viewed DESC
        LIMIT 5
    """, (user_id,))

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products

def get_user_preferences(user_id):

    connection = get_connection()

    cursor = connection.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute("""
        SELECT
            p.category,
            COUNT(*) AS category_count
        FROM user_activity ua
        JOIN products p
        ON ua.product_id = p.id
        WHERE ua.user_id = %s
        AND ua.activity_type = 'view'
        GROUP BY p.category
        ORDER BY category_count DESC
    """, (user_id,))

    preferences = cursor.fetchall()

    cursor.close()
    connection.close()

    return preferences
def get_user_viewed_product_ids(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT product_id
        FROM user_activity
        WHERE user_id = %s
        AND activity_type = 'view'
    """, (user_id,))

    product_ids = [
        row[0]
        for row in cursor.fetchall()
    ]

    cursor.close()
    connection.close()

    return product_ids