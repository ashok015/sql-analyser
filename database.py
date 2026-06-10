import sqlite3
import json
from datetime import datetime, timedelta
import os

DB_PATH = 'database.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    if os.path.exists(DB_PATH):
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            city TEXT,
            country TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            order_date DATE,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    # Sample data
    customers = [
        (1, 'John Doe', 'john@example.com', 'New York', 'USA'),
        (2, 'Jane Smith', 'jane@example.com', 'London', 'UK'),
        (3, 'Bob Johnson', 'bob@example.com', 'Toronto', 'Canada'),
        (4, 'Alice Brown', 'alice@example.com', 'Sydney', 'Australia'),
        (5, 'Charlie Wilson', 'charlie@example.com', 'Berlin', 'Germany'),
    ]
    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?, ?)', customers)

    products = [
        (1, 'Laptop', 'Electronics', 999.99, 50),
        (2, 'Mouse', 'Electronics', 29.99, 200),
        (3, 'Keyboard', 'Electronics', 79.99, 150),
        (4, 'Monitor', 'Electronics', 299.99, 80),
        (5, 'USB Cable', 'Accessories', 9.99, 500),
    ]
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?)', products)

    orders = [
        (1, 1, 1, 1, '2024-01-15'),
        (2, 2, 2, 3, '2024-01-20'),
        (3, 1, 3, 1, '2024-02-10'),
        (4, 3, 1, 2, '2024-02-15'),
        (5, 4, 4, 1, '2024-03-01'),
        (6, 2, 5, 10, '2024-03-05'),
        (7, 5, 2, 2, '2024-03-10'),
    ]
    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?)', orders)

    conn.commit()
    conn.close()
    print("Database initialized successfully")

def get_schema_description():
    return """
    Database Schema:

    customers (id, name, email, city, country)
    products (id, name, category, price, stock)
    orders (id, customer_id, product_id, quantity, order_date)

    Relationships:
    - orders.customer_id -> customers.id
    - orders.product_id -> products.id
    """

def execute_query(sql):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results], None
    except Exception as e:
        return None, str(e)
