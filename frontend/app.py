import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret-key-for-flash-messages"

API_URL = "http://127.0.0.1:8000"


# Главная страница - список книг
@app.route("/")
def index():
    try:
        response = requests.get(f"{API_URL}/books")
        if response.status_code == 200:
            books = response.json()
        else:
            books = []
            flash("Ошибка получения данных с сервера", "error")
    except requests.exceptions.ConnectionError:
        books = []
        flash("Не удалось подключиться к API серверу. Убедитесь, что backend запущен", "error")

    return render_template("index.html", books=books)


# Просмотр одной книги
@app.route("/book/<int:book_id>")
def view_book(book_id):
    try:
        response = requests.get(f"{API_URL}/books/{book_id}")
        if response.status_code == 200:
            book = response.json()
            return render_template("view.html", book=book)
        else:
            flash("Книга не найдена", "error")
            return redirect(url_for("index"))
    except requests.exceptions.ConnectionError:
        flash("Ошибка подключения к серверу", "error")
        return redirect(url_for("index"))


# Форма добавления книги
@app.route("/create", methods=["GET", "POST"])
def create_book():
    if request.method == "POST":
        try:
            data = {
                "title": request.form.get("title"),
                "author": request.form.get("author"),
                "year": int(request.form.get("year")),
                "publisher": request.form.get("publisher"),
                "pages": int(request.form.get("pages")),
                "isbn": request.form.get("isbn"),
                "quantity": int(request.form.get("quantity")),
                "price": float(request.form.get("price"))
            }

            response = requests.post(f"{API_URL}/books", json=data)

            if response.status_code == 201:
                flash("Книга успешно добавлена", "success")
                return redirect(url_for("index"))
            else:
                flash(f"Ошибка: {response.json().get('detail', 'Неизвестная ошибка')}", "error")
        except ValueError as e:
            flash(f"Ошибка преобразования данных: {e}", "error")
        except requests.exceptions.ConnectionError:
            flash("Ошибка подключения к серверу", "error")

    return render_template("create.html")


# Форма редактирования книги
@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    if request.method == "POST":
        try:
            data = {
                "title": request.form.get("title"),
                "author": request.form.get("author"),
                "year": int(request.form.get("year")),
                "publisher": request.form.get("publisher"),
                "pages": int(request.form.get("pages")),
                "isbn": request.form.get("isbn"),
                "quantity": int(request.form.get("quantity")),
                "price": float(request.form.get("price"))
            }

            response = requests.put(f"{API_URL}/books/{book_id}", json=data)

            if response.status_code == 200:
                flash("Книга успешно обновлена", "success")
                return redirect(url_for("index"))
            else:
                flash(f"Ошибка: {response.json().get('detail', 'Неизвестная ошибка')}", "error")
        except ValueError as e:
            flash(f"Ошибка преобразования данных: {e}", "error")
        except requests.exceptions.ConnectionError:
            flash("Ошибка подключения к серверу", "error")

    # GET запрос - получаем данные книги для заполнения формы
    try:
        response = requests.get(f"{API_URL}/books/{book_id}")
        if response.status_code == 200:
            book = response.json()
            return render_template("edit.html", book=book)
        else:
            flash("Книга не найдена", "error")
            return redirect(url_for("index"))
    except requests.exceptions.ConnectionError:
        flash("Ошибка подключения к серверу", "error")
        return redirect(url_for("index"))


# Удаление книги
@app.route("/delete/<int:book_id>")
def delete_book(book_id):
    try:
        response = requests.delete(f"{API_URL}/books/{book_id}")
        if response.status_code == 200:
            flash("Книга успешно удалена", "success")
        else:
            flash("Ошибка при удалении книги", "error")
    except requests.exceptions.ConnectionError:
        flash("Ошибка подключения к серверу", "error")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)