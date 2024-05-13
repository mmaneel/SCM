import cx_Oracle

# Remplacez ces informations par vos propres détails de connexion
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="orcl")
user = "C##soun"
password = "soun"

def create_commande(p_nom_client, p_prenom_client, p_num_tel, p_numero_carte, p_cvv, p_date_exp, p_balance, p_type_id, p_adresse, p_code_postal, p_produit_id, p_quantite):
    """
    Cette fonction crée une nouvelle commande dans le système SCM.

    Args:
        p_nom_client (str): Nom du client
        p_prenom_client (str): Prénom du client
        p_num_tel (int): Numéro de téléphone du client
        p_numero_carte (str): Numéro de la carte du client
        p_cvv (int): Code de vérification de la carte
        p_date_exp (int): Date d'expiration de la carte (format MMYY)
        p_balance (float): Solde de la carte
        p_type_id (int): ID du type de carte (clé étrangère vers la table typeCarte)
        p_adresse (str): Adresse du client
        p_code_postal (int): Code postal du client
        p_produit_id (int): ID du produit (clé étrangère vers la table Produit)
        p_quantite (int): Quantité du produit commandé
    """
    connection = None
    cursor = None

    try:
        # Connexion à la base de données
        connection = cx_Oracle.connect(user, password, dsn)

        # Création du curseur
        cursor = connection.cursor()

        # Vérification si le client existe
        cursor.execute("SELECT id, carte_id FROM client WHERE nom_client = :p_nom_client AND prenom_client = :p_prenom_client AND num_tel = :p_num_tel", 
                       p_nom_client=p_nom_client, p_prenom_client=p_prenom_client, p_num_tel=p_num_tel)
        customer_row = cursor.fetchone()

        # Insérer le client s'il est nouveau
        if customer_row is None:
            cursor.execute("INSERT INTO client (nom_client, prenom_client, num_tel, carte_id) VALUES (:p_nom_client, :p_prenom_client, :p_num_tel, :p_numero_carte)", 
                           p_nom_client=p_nom_client, p_prenom_client=p_prenom_client, p_num_tel=p_num_tel, p_numero_carte=p_numero_carte)
            connection.commit()

            # Récupérer l'ID du nouveau client
            cursor.execute("SELECT id FROM client WHERE nom_client = :p_nom_client AND prenom_client = :p_prenom_client AND num_tel = :p_num_tel", 
                           p_nom_client=p_nom_client, p_prenom_client=p_prenom_client, p_num_tel=p_num_tel)
            customer_row = cursor.fetchone()

        # Vérifier si la carte existe
        cursor.execute("SELECT numero FROM Carte WHERE numero = :p_numero_carte", p_numero_carte=p_numero_carte)
        card_row = cursor.fetchone()

        # Insérer la carte si elle est nouvelle
        if card_row is None:
            cursor.execute("INSERT INTO Carte (numero, cvv, date_exp, balance, type_id) VALUES (:p_numero_carte, :p_cvv, :p_date_exp, :p_balance, :p_type_id)", 
                           p_numero_carte=p_numero_carte, p_cvv=p_cvv, p_date_exp=p_date_exp, p_balance=p_balance, p_type_id=p_type_id)
            connection.commit()

        # Vérifier si l'adresse existe
        cursor.execute("SELECT id FROM Address WHERE distinaire = :p_adresse AND code_postal = :p_code_postal", 
                       p_adresse=p_adresse, p_code_postal=p_code_postal)
        address_row = cursor.fetchone()

        # Insérer l'adresse si elle est nouvelle
        if address_row is None:
            cursor.execute("INSERT INTO Address (distinaire, code_postal) VALUES (:p_adresse, :p_code_postal)", 
                           p_adresse=p_adresse, p_code_postal=p_code_postal)
            connection.commit()

        # Logique supplémentaire pour insérer la commande dans la table appropriée

    finally:
        # Nettoyage des ressources
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

# Exemple d'utilisation
create_commande("De","Jne",987664321,"5555666677778888",456,623,2000,2,"456 Avenue des Fleurs, VilleB",54321,3,1)