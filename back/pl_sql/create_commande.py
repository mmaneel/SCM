import cx_Oracle

# Remplacez ces informations par vos propres détails de connexion
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="orcl")
user = "C##soun"
password = "soun"

# Connect to the database
connection = cx_Oracle.connect(user, password, dsn)
cursor = connection.cursor()

# Define the product_quantity list
product_quantity = [
    (1, 4),  # (product_id, quantity)
    (2, 3)    # (product_id, quantity)
]

# Create the Oracle object collection manually
product_quantity_type = connection.gettype("PRODUCT_QUANTITY_TYPE")
product_quantity_table = connection.gettype("PRODUCT_QUANTITY_TABLE")
print("Test =",product_quantity_type,product_quantity_table)

product_quantity_objects = product_quantity_table.newobject()
for product_id, quantity in product_quantity:
    product_quantity_object = product_quantity_type.newobject()
    product_quantity_object.PRODUCT_ID = product_id
    product_quantity_object.QUANTITY = quantity
    product_quantity_objects.append(product_quantity_object)


# Call the PL/SQL procedure
procedure_call = """
    BEGIN
        create_commande(
            :p_nom_client,
            :p_prenom_client,
            :p_num_tel,
            :p_numero_carte,
            :p_cvv,
            :p_date_exp,
            :p_balance,
            :p_type_id,
            :p_adresse,
            :p_code_postal,
            :p_product_quantity
        );
    END;
"""
cursor.execute(procedure_call, (
    'Doe',  # p_nom_client
    'Jane',  # p_prenom_client
    987654321,  # p_num_tel
    '5555666677778888',  # p_numero_carte (nouvelle)
    456,  # p_cvv
    623,  # p_date_exp (format MMYY)
    1000000,  # p_balance
    2,  # p_type_id (PayPal)
    '456 Avenue des Fleurs, VilleB',  # p_adresse (existante)
    54321,  # p_code_postal (existant)
    product_quantity_objects    # p_product_quantity
))

# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()