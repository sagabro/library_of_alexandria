import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
con = sqlite3.connect("my_library.db", check_same_thread=False)
con.execute("Pragma foreign_keys = ON")
cursor = con.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        category TEXT,
        date INTEGER,
        origin TEXT, 
        genre TEXT) """)
con.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL) """)
con.commit()
app = FastAPI(title="My Digital Library of Alexandria")

class book_schema(BaseModel):
    title: str
    author: str
    date: int
    origin: str
    genre: str

class author(BaseModel):
    name: str
@app.get("/")
def check_connection():
    return {"message": "connected"}


@app.get("/books")
def get_books(title: str = None):
    if title:
        cursor.execute("SELECT * FROM books WHERE title = ?", (title,))
    else:
        cursor.execute("SELECT * FROM books")
    return {"books": cursor.fetchall()}
@app.post("/books")
def add_book(book:book_schema):
    cursor.execute("INSERT INTO books"
    "(title, author, date, origin, genre) VALUES (?, ?, ?, ?, ?)",
(book.title, book.author, book.date, book.origin, book.genre))
    con.commit()
    return {"message": "Book added successfully"}
