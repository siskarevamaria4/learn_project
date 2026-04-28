from fastapi import FastAPI, HTTPException, status
from database import init_db
import crud
from schemas import BookCreate, BookUpdate, BookPatch, BookRead
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Library API", description="API для управления библиотекой книг")


@app.on_event("startup")
def startup():
    init_db()


class DeleteMultipleRequest(BaseModel):
    ids: List[int]


@app.get("/books", response_model=list[BookRead])
def get_books():
    return crud.get_all_books()


@app.get("/books/{book_id}", response_model=BookRead)
def get_book(book_id: int):
    book = crud.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    book_id = crud.create_book(book.model_dump())
    return {"message": "Книга успешно добавлена", "id": book_id}


@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate):
    updated = crud.update_book(book_id, book.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return {"message": "Книга успешно обновлена"}


@app.patch("/books/{book_id}")
def patch_book(book_id: int, book: BookPatch):
    update_data = {k: v for k, v in book.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления")
    updated = crud.patch_book(book_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return {"message": "Книга успешно обновлена"}


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    deleted = crud.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return {"message": "Книга успешно удалена"}


@app.delete("/books/delete-many")
def delete_multiple_books(req: DeleteMultipleRequest):
    """Удаление нескольких книг сразу"""
    if not req.ids:
        raise HTTPException(status_code=400, detail="Список ID не может быть пустым")
    deleted = crud.delete_multiple_books(req.ids)
    return {"message": f"Удалено {deleted} книг", "deleted_count": deleted}