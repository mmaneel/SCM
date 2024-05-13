import cx_Oracle

# Replace these with your own connection details
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="orcl")
user = "C##soun"
password = "soun"

# Connect to the database
connection = cx_Oracle.connect(user, password, dsn)
cursor = connection.cursor()

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
    cursor.execute("UPDATE commande SET status = 2 WHERE id = 61")
    for line in dbms_lines(cursor):
        print(line)


execute_proc(cursor)


# Close the cursor and connection
cursor.close()
connection.close()