#!/usr/bin/env python3
"""
Script to create sample SQLite databases for testing the Database Explorer workshop
"""

import sqlite3
from pathlib import Path


def create_ecommerce_db():
    """Create a sample e-commerce database with customers, products, and orders"""
    db_path = Path("sample_ecommerce.db")

    # Remove existing database to start fresh
    if db_path.exists():
        db_path.unlink()

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                city TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                category TEXT,
                stock_quantity INTEGER DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_amount DECIMAL(10,2),
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')

        # Insert sample data
        customers_data = [
            ('Alice Johnson', 'alice@email.com', 'New York'),
            ('Bob Smith', 'bob@email.com', 'Los Angeles'),
            ('Charlie Brown', 'charlie@email.com', 'Chicago'),
            ('Diana Ross', 'diana@email.com', 'Miami'),
            ('Edward Wilson', 'edward@email.com', 'Seattle')
        ]

        cursor.executemany(
            'INSERT INTO customers (name, email, city) VALUES (?, ?, ?)',
            customers_data
        )

        products_data = [
            ('Laptop', 999.99, 'Electronics', 50),
            ('Smartphone', 699.99, 'Electronics', 100),
            ('Coffee Mug', 12.99, 'Kitchen', 200),
            ('Desk Chair', 249.99, 'Furniture', 25),
            ('Book: Python Programming', 39.99, 'Books', 75)
        ]

        cursor.executemany(
            'INSERT INTO products (name, price, category, stock_quantity) VALUES (?, ?, ?, ?)',
            products_data
        )

        orders_data = [
            (1, 1, 1, 999.99),   # Alice bought a laptop
            (2, 2, 1, 699.99),   # Bob bought a smartphone
            (1, 3, 2, 25.98),    # Alice bought 2 coffee mugs
            (3, 4, 1, 249.99),   # Charlie bought a desk chair
            (4, 5, 1, 39.99),    # Diana bought a book
            (5, 1, 1, 999.99),   # Edward bought a laptop
            (2, 3, 3, 38.97),    # Bob bought 3 coffee mugs
        ]

        cursor.executemany(
            'INSERT INTO orders (customer_id, product_id, quantity, total_amount) VALUES (?, ?, ?, ?)',
            orders_data
        )

        # Create some indexes for optimization examples
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_customer_email ON customers(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_product_category ON products(category)')

        conn.commit()
        print(f"✅ Created {db_path} with sample e-commerce data")


def create_library_db():
    """Create a sample library database with books, authors, and borrowers"""
    db_path = Path("sample_library.db")

    # Remove existing database to start fresh
    if db_path.exists():
        db_path.unlink()

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                birth_year INTEGER,
                nationality TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                publication_year INTEGER,
                isbn TEXT UNIQUE,
                pages INTEGER,
                available BOOLEAN DEFAULT 1,
                FOREIGN KEY (author_id) REFERENCES authors (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE borrowers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                library_card TEXT UNIQUE NOT NULL,
                email TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                borrower_id INTEGER NOT NULL,
                loan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date DATE,
                return_date DATE,
                FOREIGN KEY (book_id) REFERENCES books (id),
                FOREIGN KEY (borrower_id) REFERENCES borrowers (id)
            )
        ''')

        # Insert sample data
        authors_data = [
            ('George Orwell', 1903, 'British'),
            ('J.K. Rowling', 1965, 'British'),
            ('Stephen King', 1947, 'American'),
            ('Agatha Christie', 1890, 'British'),
            ('Ernest Hemingway', 1899, 'American')
        ]

        cursor.executemany(
            'INSERT INTO authors (name, birth_year, nationality) VALUES (?, ?, ?)',
            authors_data
        )

        books_data = [
            ('1984', 1, 1949, '978-0-452-28423-4', 328, 1),
            ('Animal Farm', 1, 1945, '978-0-452-28424-1', 112, 1),
            ('Harry Potter and the Philosopher\'s Stone', 2, 1997, '978-0-7475-3269-9', 223, 0),
            ('The Shining', 3, 1977, '978-0-385-12167-5', 447, 1),
            ('Murder on the Orient Express', 4, 1934, '978-0-06-207350-4', 256, 1),
            ('The Old Man and the Sea', 5, 1952, '978-0-684-80122-3', 127, 1)
        ]

        cursor.executemany(
            'INSERT INTO books (title, author_id, publication_year, isbn, pages, available) VALUES (?, ?, ?, ?, ?, ?)',
            books_data
        )

        borrowers_data = [
            ('John Doe', 'LC001', 'john.doe@email.com'),
            ('Jane Smith', 'LC002', 'jane.smith@email.com'),
            ('Mike Johnson', 'LC003', 'mike.johnson@email.com')
        ]

        cursor.executemany(
            'INSERT INTO borrowers (name, library_card, email) VALUES (?, ?, ?)',
            borrowers_data
        )

        loans_data = [
            (3, 1, '2024-01-15', '2024-02-15', None),  # John borrowed Harry Potter (not returned)
            (1, 2, '2024-01-20', '2024-02-20', '2024-02-18'),  # Jane borrowed 1984 (returned)
            (4, 3, '2024-02-01', '2024-03-01', None),  # Mike borrowed The Shining (not returned)
        ]

        cursor.executemany(
            'INSERT INTO loans (book_id, borrower_id, loan_date, due_date, return_date) VALUES (?, ?, ?, ?, ?)',
            loans_data
        )

        conn.commit()
        print(f"✅ Created {db_path} with sample library data")


if __name__ == "__main__":
    print("Creating sample databases for Database Explorer workshop...")
    create_ecommerce_db()
    create_library_db()
    print("✅ All sample databases created successfully!")
    print("\nUse these databases to test the workshop tools:")
    print("- sample_ecommerce.db: customers, products, orders")
    print("- sample_library.db: authors, books, borrowers, loans")