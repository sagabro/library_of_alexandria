import sqlite3
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from contextlib import contextmanager

@contextmanager
def get_db_cursor():
    con = sqlite3.connect("my_library.db", check_same_thread=False)
    con.execute("Pragma foreign_keys = ON")
    cursor = con.cursor()
    try:
        yield cursor
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def init_db():
    with get_db_cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author_id INTEGER NOT NULL,
        category TEXT,
        date INTEGER,
        origin TEXT, 
        genre TEXT,
        FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
        UNIQUE(title, author)) """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ) """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS chapters(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        chapter_number INTEGER NOT NULL,
        title TEXT,
        body TEXT NOT NULL,
        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
        UNIQUE(book_id, chapter_number)
    );""")

init_db()
app = FastAPI(title="My Digital Library of Alexandria")

class book_schema(BaseModel):
    title: str
    author: str
    date: int
    origin: str
    genre: str

class author_schema(BaseModel):
    name: str

class chapter_schema(BaseModel):
    book_id: int
    chapter_number: int
    title: str
    body: str
@app.get("/")
def check_connection():
    return {"message": "connected"}
@app.get("/books")
def get_books(title: str = None):
    with get_db_cursor() as cursor:
        if title:
            cursor.execute("SELECT * FROM books WHERE title = ?", (title,))
        else:
            cursor.execute("SELECT * FROM books")
        return {"books": cursor.fetchall()}
@app.post("/books")
def add_book(book:book_schema):
    with get_db_cursor() as cursor:
        cursor.execute("INSERT INTO books"
        "(title, author, date, origin, genre) VALUES (?, ?, ?, ?, ?)",
            (book.title, book.author, book.date, book.origin, book.genre))
        return {"message": "Book added successfully"}
@app.post("/books/{books_title}/chapters")
def add_chapter(chapter:chapter_schema):
    with get_db_cursor() as cursor:
        cursor.execute("INSERT INTO chapters"
        "(book_id, chapter_number, title, body) VALUES (?, ?, ?, ?)",
    (chapter.book_id, chapter.chapter_number, chapter.title, chapter.body))
        return {"message": "Chapter added successfully"}
@app.delete("/books/{books_title}")
def delete_book(books_title:str):
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM books WHERE title = ?", (books_title,))
        return {"message": "Book deleted successfully"}
@app.delete("/books/{books_title}")
def delete_book(books_title:str):
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM books WHERE title = ?", (books_title,))
        return {"message": "Book deleted successfully"}