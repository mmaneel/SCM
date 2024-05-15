from .models import *
from datetime import date

def insert_data_into_database():
    # Insertion des produits
    Produit.objects.create(code_produit=1, nom_produit='IPHONE', Quantite_enStock=10, prix_unitaire=500.00, description='Smartphone dernier cri avec des fonctionnalités avancées')
    Produit.objects.create(code_produit=2, nom_produit='OPPO', Quantite_enStock=15, prix_unitaire=400.00, description='Téléphone Android abordable avec un bon rapport qualité-prix')
    Produit.objects.create(code_produit=3, nom_produit='REDMI', Quantite_enStock=20, prix_unitaire=600.00, description='iPhone haut de gamme avec un design élégant et des performances exceptionnelles')

    # Insertion des clients (si nécessaire)
    # Client.objects.create(...) 

    # Insertion des adresses (si nécessaire)
    # Address.objects.create(...) 

    # Insertion des commandes
    Commande.objects.create(commande_date=date.today(), status=1, prix_total=200, client_id=1, adresse_id=1)  # Commande du client 1 à l'adresse 1
    Commande.objects.create(commande_date=date.today(), status=1, prix_total=300, client_id=2, adresse_id=2)  # Commande du client 2 à l'adresse 2
    Commande.objects.create(commande_date=date.today(), status=1, prix_total=400, client_id=3, adresse_id=3)  # Commande du client 3 à l'adresse 3

# Call the function to execute the insertions
insert_data_into_database()
