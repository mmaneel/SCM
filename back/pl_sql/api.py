from flask import Flask, request, jsonify
from flask_cors import CORS
import cx_Oracle
from create_commande import commande_creation
from cursor_execute import *

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})

# Assuming cx_Oracle setup and connection code is already done
@app.route('/api/create_commande', methods=['POST'])
def create_commande():
    data = request.json
    p_nom_client = data.get("p_nom_client")
    p_prenom_client = data.get("p_prenom_client")
    p_num_tel = data.get("p_num_tel")
    p_numero_carte = data.get("p_numero_carte")
    p_cvv = data.get("p_cvv")
    p_date_exp = data.get("p_date_exp")
    p_balance = 1000000
    p_type_id = data.get("p_type_i")
    p_adresse = data.get("p_adresse")
    p_code_postal = data.get("p_code_postal")
    product_quantity_list = data.get("product_quantity")

    commande_creation(p_nom_client, p_prenom_client, p_num_tel, p_numero_carte, p_cvv, p_date_exp, p_balance, p_type_id, p_adresse, p_code_postal, product_quantity_list)
    return jsonify({'message': 'Order created successfully'})

# Endpoint for retrieving products
@app.route('/api/products', methods=['GET'])
def get_all_products():
    data = get_products()
    return jsonify(data)

# Endpoint for retrieving orders
@app.route('/api/orders', methods=['GET'])
def get_all_orders():
    data = get_orders()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)