import cx_Oracle

# Replace these with your actual connection details
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="orcl")
user = "C##soun"
password = "soun"

# Connect to the database
connection = cx_Oracle.connect(user, password, dsn)
cursor = connection.cursor()

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

products = []


# Fetch and print the output for Listing Orders

def dbms_lines( cursor):
    status = cursor.var( cx_Oracle.NUMBER)
    line   = cursor.var( cx_Oracle.STRING)

    lines = []
    while True:
        cursor.callproc( 'DBMS_OUTPUT.GET_LINE', (line, status))
        if status.getvalue() == 0:
            lines.append( line.getvalue())
        else:
            break

    return lines

def execute_proc(cursor,proc):
    cursor.callproc("dbms_output.enable")
    
    # Execute the cursor for Listing Orders
    cursor.execute(proc)

    for line in dbms_lines(cursor):
        print(line)

print("Testing the cursor 1")

execute_proc(cursor,orders_cursor)

print("Testing the cursor 2")

execute_proc(cursor,products_cursor)



# Close the cursor and connection
cursor.close()
connection.close()
