from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
from models import create_sushi, add_order, get_orders, clear_all_data, is_sushi_table_empty

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Check if the Sushi table is empty before adding sushi items
if is_sushi_table_empty():
    create_sushi("Sushi A", 3.0)
    create_sushi("Sushi B", 4.0)

@app.route("/add-order", methods=["POST"])
def add_order_endpoint():
    sushi_items = request.json.get("sushi_items", {})
    add_order(sushi_items)
    return jsonify({"message": "Order added successfully"}), 201

@app.route("/get-orders", methods=["GET"])
def get_orders_endpoint():
    orders = get_orders()
    return jsonify({"orders": orders}), 200

@app.route("/clear-all", methods=["DELETE"])
def clear_all_endpoint():
    clear_all_data()
    return jsonify({"message": "All data cleared successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
