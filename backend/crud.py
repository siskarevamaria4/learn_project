from database import get_connection


# CREATE - Добавление книги
def create_book(data: dict) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, year, publisher, pages, isbn, quantity, price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["title"], data["author"], data["year"],
        data["publisher"], data["pages"], data["isbn"],
        data["quantity"], data["price"]
    ))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


# READ - Получить все книги
def get_all_books():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM books ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]


# READ - Получить книгу по ID
def get_book_by_id(book_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# UPDATE - Полное обновление книги
def update_book(book_id: int, data: dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books 
        SET title = ?, author = ?, year = ?, publisher = ?, 
            pages = ?, isbn = ?, quantity = ?, price = ?
        WHERE id = ?
    """, (
        data["title"], data["author"], data["year"],
        data["publisher"], data["pages"], data["isbn"],
        data["quantity"], data["price"], book_id
    ))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


# UPDATE - Частичное обновление
def patch_book(book_id: int, data: dict) -> bool:
    conn = get_connection()

    # Получаем текущие данные книги
    current = get_book_by_id(book_id)
    if not current:
        conn.close()
        return False

    # Обновляем только переданные поля
    for key, value in data.items():
        if value is not None:
            current[key] = value

    # Сохраняем обновлённые данные
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books 
        SET title = ?, author = ?, year = ?, publisher = ?, 
            pages = ?, isbn = ?, quantity = ?, price = ?
        WHERE id = ?
    """, (
        current["title"], current["author"], current["year"],
        current["publisher"], current["pages"], current["isbn"],
        current["quantity"], current["price"], book_id
    ))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


# DELETE - Удаление книги
def delete_book(book_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted