from database import get_connection
import json


def create_book(data: dict) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, year, publisher, pages, isbn, quantity, genre)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (data["title"], data["author"], data["year"], data["publisher"],
          data["pages"], data["isbn"], data["quantity"], data["genre"]))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_books():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM books ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_book_by_id(book_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_book(book_id: int, data: dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books 
        SET title = ?, author = ?, year = ?, publisher = ?, 
            pages = ?, isbn = ?, quantity = ?, genre = ?
        WHERE id = ?
    """, (data["title"], data["author"], data["year"], data["publisher"],
          data["pages"], data["isbn"], data["quantity"], data["genre"], book_id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def patch_book(book_id: int, data: dict) -> bool:
    conn = get_connection()
    current = get_book_by_id(book_id)
    if not current:
        conn.close()
        return False
    for key, value in data.items():
        if value is not None:
            current[key] = value
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books 
        SET title = ?, author = ?, year = ?, publisher = ?, 
            pages = ?, isbn = ?, quantity = ?, genre = ?
        WHERE id = ?
    """, (current["title"], current["author"], current["year"], current["publisher"],
          current["pages"], current["isbn"], current["quantity"], current["genre"], book_id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def delete_book(book_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def delete_multiple_books(book_ids: list[int]) -> int:
    """Удаление нескольких книг по списку ID, возвращает количество удалённых записей."""
    if not book_ids:
        return 0
    conn = get_connection()
    cursor = conn.cursor()
    # Создаём параметризованный запрос с количеством плейсхолдеров
    placeholders = ','.join('?' * len(book_ids))
    query = f"DELETE FROM books WHERE id IN ({placeholders})"
    cursor.execute(query, book_ids)
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted