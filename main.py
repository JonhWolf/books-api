from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Book Library API")

# Хранилище книг в памяти
books = []
next_id = 1

# Модель данных книги
class BookData(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int = Field(ge=1, le=2100)

# Получить все книги
@app.get("/books")
def get_books():
    return books

# Получить книгу по ID
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Добавить книгу
@app.post("/books", status_code=201)
def add_book(book: BookData):
    global next_id

    new_book = {
        "id": next_id,
        **book.model_dump()
    }
    books.append(new_book)
    next_id += 1
    return new_book

# Обновить книгу
@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookData):
    for existing_book in books:
        if existing_book["id"] == book_id:
            existing_book.update(book.model_dump())
            return existing_book
    raise HTTPException(status_code=404, detail="Book not found")

# Удалить книгу
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")
