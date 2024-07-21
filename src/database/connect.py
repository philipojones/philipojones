"""
Database connection logic goes here

- Connect to the database

Keep the database URL in the .env file

"""
from fastapi import FastAPI, HTTPException
import sqlite3
import os

# Determine the absolute path to the database file
DB_FILE = os.path.join(os.path.dirname(__file__), '../databases/books.db')

app = FastAPI()
# SQLite database connection setup

# SQLite database connection
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create books table (run this only once)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        category TEXT
    )
""")
conn.commit()

# Create (POST)
@app.post('/books/create_book')
async def create_book(title: str, author: str, category: str):
    cursor.execute("INSERT INTO books (title, author, category) VALUES (?, ?, ?)", (title, author, category))
    conn.commit()
    return {"message": "Book created successfully"}

# Read (GET)
@app.get('/books')
async def read_all_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return books

# Update (PUT)
@app.put('/books/update_book/{book_id}')
async def update_book(book_id: int, title: str, author: str, category: str):
    cursor.execute("UPDATE books SET title=?, author=?, category=? WHERE id=?", (title, author, category, book_id))
    conn.commit()
    return {"message": "Book updated successfully"}

# Delete (DELETE)
@app.delete('/books/delete_book/{book_id}')
async def delete_book(book_id: int):
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    return {"message": "Book deleted successfully"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
