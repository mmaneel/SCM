import cx_Oracle
from common import * 


def get_orders():
    # Replace these with your actual connection details
    connection,cursor = connect()

    # Cursor for Listing Orders
    orders_cursor = """
        DECLARE
            CURSOR orders_cursor IS
                SELECT c.nom_client, c.prenom_client, c.num_tel, cmd.id, cmd.commande_date, cmd.prix_total
                FROM client c
                JOIN commande cmd ON c.id = cmd.id_client;
        BEGIN
            FOR order_row IN orders_cursor LOOP
                DBMS_OUTPUT.PUT_LINE('Client: ' || order_row.nom_client || ' ' || order_row.prenom_client || ', Numéro de téléphone: ' || order_row.num_tel || ', Commande ID: ' || order_row.id || ', Date: ' || order_row.commande_date || ', Total: ' || order_row.prix_total);
            END LOOP;
        EXCEPTION
            WHEN OTHERS THEN
                DBMS_OUTPUT.PUT_LINE('An error occurred: ' || SQLERRM);
        END;
    """

    cursor.callproc("dbms_output.enable")
    
    # Execute the cursor for Listing Orders
    cursor.execute(orders_cursor)

    orders = []
    lines = dbms_lines(cursor)

    # Close the cursor and connection
    disconnect(connection,cursor)

    for line in lines:
        client_name = line.split('Client: ')[1].split(',')[0].strip()
        client_phone = line.split('Numéro de téléphone: ')[1].split(',')[0].strip()
        order_id = int(line.split('Commande ID: ')[1].split(',')[0].strip())
        order_date = line.split('Date: ')[1].split(',')[0].strip()
        order_total = float(line.split('Total: ')[1].strip())

        # Append order to the orders list
        orders.append({"client": client_name, "phone": client_phone, "id": order_id, "date": order_date, "total": order_total})

    return orders





def get_products(): 
    # Replace these with your actual connection details
    connection,cursor = connect()

    # Cursor for Listing Products
    products_cursor = """
        DECLARE
            CURSOR products_cursor IS
                SELECT id, nom_produit, Quantite_enStock
                FROM Produit;
        BEGIN
            FOR product_row IN products_cursor LOOP
                DBMS_OUTPUT.PUT_LINE('Produit ID: ' || product_row.id || ', Nom: ' || product_row.nom_produit || ', Quantité en stock: ' || product_row.Quantite_enStock);
            END LOOP;
        EXCEPTION
            WHEN OTHERS THEN
                DBMS_OUTPUT.PUT_LINE('An error occurred: ' || SQLERRM);
        END;
    """

    cursor.callproc("dbms_output.enable")
    
    # Execute the cursor for Listing Orders
    cursor.execute(products_cursor)

    products = []
    lines = dbms_lines(cursor)

    # Close the cursor and connection
    disconnect(connection,cursor)

    for line in lines:
        # Extract product information from each line
        parts = line.split(',')
        product_id = int(parts[0].split(':')[1].strip())
        product_name = parts[1].split(':')[1].strip()
        product_quantity = int(parts[2].split(':')[1].strip())

        # Append product to the products list
        products.append({"id": product_id, "nom": product_name, "qte": product_quantity})

    return products




    
