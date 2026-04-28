from pydantic import BaseModel, Field
from typing import Optional, Literal

# Допустимые жанры
Genre = Literal[
    "Роман", "Детектив", "Фантастика", "Фэнтези",
    "Научная литература", "Поэзия", "Драма", "Приключения",
    "Триллер", "Ужасы", "Биография", "История"
]


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1450, le=2025)
    publisher: str = Field(..., min_length=1, max_length=100)
    pages: int = Field(..., ge=1, le=5000)
    isbn: str = Field(..., min_length=10, max_length=13)
    quantity: int = Field(..., ge=0)
    genre: Genre


class BookUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1450, le=2025)
    publisher: str = Field(..., min_length=1, max_length=100)
    pages: int = Field(..., ge=1, le=5000)
    isbn: str = Field(..., min_length=10, max_length=13)
    quantity: int = Field(..., ge=0)
    genre: Genre


class BookPatch(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1450, le=2025)
    publisher: Optional[str] = Field(None, min_length=1, max_length=100)
    pages: Optional[int] = Field(None, ge=1, le=5000)
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)
    quantity: Optional[int] = Field(None, ge=0)
    genre: Optional[Genre] = None


class BookRead(BaseModel):
    id: int
    title: str
    author: str
    year: int
    publisher: str
    pages: int
    isbn: str
    quantity: int
    genre: str