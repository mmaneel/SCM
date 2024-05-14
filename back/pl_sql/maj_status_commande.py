import cx_Oracle
from common import * 


def maj_statut_commande(p_commande_id, p_nouveau_statut):

    connection,cursor = connect()

    # Call the PL/SQL procedure
    procedure_call = """
        BEGIN
            maj_statut_commande(:p_commande_id, :p_nouveau_statut);
        END;
    """

    cursor.callproc("dbms_output.enable")
   
    cursor.execute(procedure_call, (p_commande_id, p_nouveau_statut))

    result = []

    lines = dbms_lines(cursor)

    disconnect(connection,cursor)
    
    result.append({"result": lines})

    return result

