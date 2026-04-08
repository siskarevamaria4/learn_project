def get_status_data():
    return {
        "status": "ok",
        "message": "Backend работает",
        "service": "backend-service",
        "items_count": 3
    }


def get_items_data():
    return [
        {"id": 1, "name": "Телефоны"},
        {"id": 2, "name": "Наушники"},
        {"id": 3, "name": "Плашеты"},
        {"id": 4, "name": "Компьютеры"}
    ]