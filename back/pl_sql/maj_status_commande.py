import cx_Oracle

# Remplacez ces informations par vos propres détails de connexion
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="orcl")
user = "C##soun"
password = "soun"

# Connect to the database
connection = cx_Oracle.connect(user, password, dsn)
cursor = connection.cursor()

# Call the PL/SQL procedure
procedure_call = """
    BEGIN
        maj_statut_commande(:p_commande_id, :p_nouveau_statut);
    END;
"""

# Define the command IDs and new statuses
commands = [
    (47, 5),
    (48, 5),
    (1, 2),
    (2, 3),
    (3, 4)
]

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

def execute_proc(cursor):
    cursor.callproc("dbms_output.enable")
    
    for commande_id, nouveau_statut in commands:
        cursor.execute(procedure_call, (commande_id, nouveau_statut))

    for line in dbms_lines(cursor):
        print(line)


execute_proc(cursor)




# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
