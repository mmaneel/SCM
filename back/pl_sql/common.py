import cx_Oracle

def connect(): 
    # Remplacez ces informations par vos propres détails de connexion
    dsn = cx_Oracle.makedsn("localhost", 1522, service_name="orcl")
    user = "manel"
    password = "serine"

    # Connect to the database
    connection = cx_Oracle.connect(user, password, dsn)
    cursor = connection.cursor()
    return connection,cursor


def disconnect(connection,cursor):
    # Commit the changes
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

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

