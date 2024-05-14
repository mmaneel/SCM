import cx_Oracle
from common import * 

def commande_creation(p_nom_client,p_prenom_client,p_num_tel,p_numero_carte,p_cvv,p_date_exp,p_balance,p_type_id,p_adresse,p_code_postal,product_quantity):
    connection,cursor = connect()

    # Create the Oracle object collection manually
    product_quantity_type = connection.gettype("PRODUCT_QUANTITY_TYPE")
    product_quantity_table = connection.gettype("PRODUCT_QUANTITY_TABLE")

    product_quantity_objects = product_quantity_table.newobject()
    for item in product_quantity:
        product_id = item['productId']
        quantity = item['quantity']
    for item in product_quantity:
        product_id = item['productId']
        quantity = item['quantity']
        product_quantity_object = product_quantity_type.newobject()
        product_quantity_object.PRODUCT_ID = product_id
        product_quantity_object.QUANTITY = quantity
        product_quantity_objects.append(product_quantity_object)

    print(product_quantity_objects)

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
        p_nom_client,
        p_prenom_client, 
        p_num_tel,  
        p_numero_carte,  
        p_cvv,  
        p_date_exp,
        p_balance,
        p_type_id,
        p_adresse,
        p_code_postal,
        product_quantity_objects    # p_product_quantity
    ))

    disconnect(connection,cursor)




