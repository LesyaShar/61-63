from flask import Flask, jsonify, request
from db import get_db_connection

app = Flask(__name__)

# --- ЭНДПОИНТ 1: Главная страница (проверка, что сервер работает) ---
@app.route('/')
def index():
    return jsonify({"message": "API интернет-магазина 'В стране книг' работает!"})

# --- ЭНДПОИНТ 2: Получить все товары (книги) ---
@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Не удалось подключиться к БД"}), 500

    cursor = conn.cursor()
    # Запрос: берем товары и присоединяем название категории
    query = """
        SELECT p.ProductID, p.Title, p.Author, p.Price, p.StockQuantity, c.CategoryName
        FROM Products p
        LEFT JOIN Categories c ON p.CategoryID = c.CategoryID
        WHERE p.IsAvailable = 1
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    # Преобразуем результат в список словарей (JSON)
    products = []
    for row in rows:
        products.append({
            "id": row.ProductID,
            "title": row.Title,
            "author": row.Author,
            "price": float(row.Price),
            "stock": row.StockQuantity,
            "category": row.CategoryName
        })

    cursor.close()
    conn.close()
    return jsonify(products)

# --- ЭНДПОИНТ 3: Получить все услуги ---
@app.route('/api/services', methods=['GET'])
def get_services():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Не удалось подключиться к БД"}), 500

    cursor = conn.cursor()
    query = "SELECT ServiceID, ServiceName, Description, Price FROM Services"
    cursor.execute(query)
    rows = cursor.fetchall()

    services = []
    for row in rows:
        services.append({
            "id": row.ServiceID,
            "name": row.ServiceName,
            "description": row.Description,
            "price": float(row.Price)
        })

    cursor.close()
    conn.close()
    return jsonify(services)

# --- ЭНДПОИНТ 4: Получить заказы конкретного пользователя ---
@app.route('/api/users/<int:user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Не удалось подключиться к БД"}), 500

    cursor = conn.cursor()
    query = """
        SELECT o.OrderID, o.OrderDate, o.Status, o.TotalAmount, dm.DeliveryName
        FROM Orders o
        LEFT JOIN DeliveryMethods dm ON o.DeliveryMethodID = dm.DeliveryMethodID
        WHERE o.UserID = ?
    """
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()

    orders = []
    for row in rows:
        orders.append({
            "order_id": row.OrderID,
            "date": str(row.OrderDate),
            "status": row.Status,
            "total": float(row.TotalAmount),
            "delivery": row.DeliveryName
        })

    cursor.close()
    conn.close()
    return jsonify(orders)

# --- ЗАПУСК СЕРВЕРА ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)