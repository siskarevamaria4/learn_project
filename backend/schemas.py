from pydantic import BaseModel, Field
from typing import Optional

# Схема для создания книги (POST)
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Название книги")
    author: str = Field(..., min_length=1, max_length=100, description="Автор")
    year: int = Field(..., ge=1450, le=2025, description="Год издания")
    publisher: str = Field(..., min_length=1, max_length=100, description="Издательство")
    pages: int = Field(..., ge=1, le=5000, description="Количество страниц")
    isbn: str = Field(..., min_length=10, max_length=13, description="ISBN")
    quantity: int = Field(..., ge=0, description="Количество экземпляров")
    price: float = Field(..., gt=0, description="Цена")

# Схема для полного обновления (PUT)
class BookUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1450, le=2025)
    publisher: str = Field(..., min_length=1, max_length=100)
    pages: int = Field(..., ge=1, le=5000)
    isbn: str = Field(..., min_length=10, max_length=13)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., gt=0)

# Схема для частичного обновления (PATCH)
class BookPatch(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1450, le=2025)
    publisher: Optional[str] = Field(None, min_length=1, max_length=100)
    pages: Optional[int] = Field(None, ge=1, le=5000)
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, gt=0)

# Схема для чтения (ответ сервера)
class BookRead(BaseModel):
    id: int
    title: str
    author: str
    year: int
    publisher: str
    pages: int
    isbn: str
    quantity: int
    price: float