import cx_Oracle
from common import * 

connection,cursor = connect()

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
disconnect(connection,cursor)