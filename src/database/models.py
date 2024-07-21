"""
The models

The models are the classes that define the structure of the database tables.

The models are defined using the SQLModel class, which is a class that comes from the SQLModel library.

Define the querying logics in particular model
"""
import sqlite3
from typing import Optional

class User:
    def __init__(self, username: str, email: str, hashed_password: str,
                 is_active: bool, is_superuser: bool,
                 id_type: Optional[str] = None, id_number: Optional[str] = None):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.id_type = id_type
        self.id_number = id_number

    def save(self):
        conn = sqlite3.connect("books.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, email, hashed_password, is_active, is_superuser, id_type, id_number)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.username, self.email, self.hashed_password, self.is_active, self.is_superuser, self.id_type, self.id_number))
        conn.commit()
        conn.close()

    def update(self, **kwargs):
        conn = sqlite3.connect("books.db")
        cursor = conn.cursor()
        set_clause = ', '.join(f'{key} = ?' for key in kwargs.keys())
        values = list(kwargs.values())
        values.append(self.username)  # Use username to identify the user to update
        cursor.execute(f"""
            UPDATE users
            SET {set_clause}
            WHERE username = ?
        """, (*values,))
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect("books.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=?", (self.username,))
        conn.commit()
        conn.close()

    @classmethod
    def by_username(cls, username: str) -> Optional["User"]:
        conn = sqlite3.connect("books.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(*row)
        return None

def create_tables():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            hashed_password TEXT NOT NULL,
            is_active INTEGER,
            is_superuser INTEGER,
            id_type TEXT,
            id_number TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# Call create_tables() to create the SQLite table if it doesn't exist
create_tables()
