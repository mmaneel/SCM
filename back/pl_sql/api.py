from flask import Flask, request, jsonify
import cx_Oracle
from create_commande import *

app = Flask(__name__)

# Assuming cx_Oracle setup and connection code is already done

@app.route('/api/create_commande', methods=['POST'])
def create_commande():
    data = request.json
    
    # Extract data from JSON
    p_nom_client = data.get("p_prenom_client")
    p_prenom_client = data.get("p_nom_client")
    p_num_tel = data.get("p_num_tel")
    p_numero_carte = data.get("p_numero_carte")
    p_cvv = data.get("p_cvv")
    p_date_exp = data.get("p_date_exp")
    p_balance = 1000000
    p_type_id = data.get("p_type_i")
    p_adresse = data.get("p_adresse")
    p_code_postal = data.get("p_code_postal")
    product_quantity = data.get("product_quantity")

    commande_creation(p_nom_client,p_prenom_client,p_num_tel,p_numero_carte,p_cvv,p_date_exp,p_balance,p_type_id,p_adresse,p_code_postal,product_quantity)
    
    return jsonify({'message': 'Order created successfully'})


# Endpoint for retrieving products
@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(get_products())


# Endpoint for retrieving orders
@app.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify(get_orders())


if __name__ == '__main__':
    app.run(debug=True)
