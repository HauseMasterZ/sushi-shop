from database import get_database_connection

def create_sushi(name, price):
    conn = get_database_connection()
    cursor = conn.cursor()
    query = "INSERT INTO Sushi (name, price) VALUES (%s, %s)"
    cursor.execute(query, (name, price))
    conn.commit()
    conn.close()

def add_order(sushi_items):
    conn = get_database_connection()
    cursor = conn.cursor()

    # Calculate the total price and apply discounts
    total_price, discount_applied, discount_amount = calculate_price_with_discounts(sushi_items)
    # Insert into Orders table
    query = "INSERT INTO Orders (total_price, discount_applied, discount_amount) VALUES (%s, %s, %s)"
    cursor.execute(query, (total_price, discount_applied, discount_amount))
    order_id = cursor.lastrowid

    # Insert into OrderDetails table
    for sushi_id, quantity in sushi_items.items():
        query = "INSERT INTO OrderDetails (order_id, sushi_id, quantity) VALUES (%s, %s, %s)"
        cursor.execute(query, (order_id, sushi_id, quantity))

    conn.commit()
    conn.close()


def is_sushi_table_empty():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Sushi")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0



def get_orders():
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT o.id, od.quantity, s.name, s.price, o.discount_applied, o.discount_amount, o.total_price
    FROM Orders o
    JOIN OrderDetails od ON o.id = od.order_id
    JOIN Sushi s ON od.sushi_id = s.id
    """
    cursor.execute(query)
    orders = cursor.fetchall()

    conn.close()
    return orders


def calculate_price_with_discounts(sushi_items):
    # Price definitions
    price_a = 3.0
    price_b = 4.0

    # Calculate total quantity and price
    total_quantity = sushi_items['1'] + sushi_items['2']
    total_price = (sushi_items['1'] * price_a) + (sushi_items['2'] * price_b)
    print(total_quantity, total_price)
    # Discounts
    discount_applied = "No Discount"
    discount_amount = 0.0

    # "10 Deal"
    if total_quantity >= 10:
        discount_applied = "10% Discount"
        discount_amount = total_price * 0.10
        total_price -= discount_amount

    # "20 Deal"
    if total_quantity >= 20:
        discount_applied = "20% Discount"
        discount_amount = total_price * 0.20
        total_price -= discount_amount

    # "Lunch Deal"
    from datetime import datetime
    current_time = datetime.now().time()
    if current_time.hour >= 11 and current_time.hour < 14:
        discount_applied = "Lunch Discount"
        lunch_discount = total_price * 0.20
        discount_amount += lunch_discount
        total_price -= lunch_discount

    return total_price, discount_applied, discount_amount


def clear_all_data():
    conn = get_database_connection()
    cursor = conn.cursor()

    # Clear data from OrderDetails first due to foreign key constraints
    cursor.execute("DELETE FROM OrderDetails")
    
    # Then clear data from Orders and Sushi tables
    cursor.execute("DELETE FROM Orders")
    cursor.execute("DELETE FROM Sushi")

    # Reset auto-increment for Orders and Sushi tables
    cursor.execute("ALTER TABLE Orders AUTO_INCREMENT = 1")
    cursor.execute("ALTER TABLE Sushi AUTO_INCREMENT = 1")

    # Re-add default sushi items
    create_sushi("Sushi A", 3.0)
    create_sushi("Sushi B", 4.0)

    conn.commit()
    conn.close()
