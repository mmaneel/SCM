from django.utils import timezone
from django.db import transaction
from .models import *
from django.core.serializers import serialize
import json
from django.http import JsonResponse
import time
from .decorators import calculate_execution_time
import traceback
import sys
from django.views.decorators.http import require_http_methods
from datetime import date




def create_commande(p_nom_client, p_prenom_client, p_num_tel, p_numero_carte, p_cvv, p_date_exp, p_balance, p_type_id, p_adresse, p_code_postal, list_product_qte):
    try:
        # Get the TypeCarte instance
        type_carte = TypeCarte.objects.get(id=p_type_id)

        # Check if the client already exists
        client, created = Client.objects.get_or_create(
            nom_client=p_nom_client,
            prenom_client=p_prenom_client,
            num_tel=p_num_tel
        )

        
        carte, _ = Carte.objects.get_or_create(
            numero=p_numero_carte,
            defaults={'cvv': p_cvv, 'date_exp': p_date_exp, 'balance': p_balance, 'type_carte': type_carte}
        )
        carte.client = client
        carte.save()

        # Check if the address already exists
        adresse, _ = Address.objects.get_or_create(
            distinaire=p_adresse,
            code_postal=p_code_postal
        )

        prix_total = 0 
        # Create a new order
        commande = Commande.objects.create(
            commande_date=timezone.now(),
            status=1,  # Assuming initial status is 1
            prix_total=prix_total,
            client=client,
            adresse=adresse
        )

        
        for product in list_product_qte: 
            # Retrieve product details
            produit = Produit.objects.get(id=product['produit_id'])
            prix_unitaire = produit.prix_unitaire

            # Convert string inputs to numeric types
            p_quantite = int(product['quantite'])
            prix_unitaire = float(prix_unitaire)
            
            # Check_stock_availability
            if (p_quantite > produit.Quantite_enStock) :
                return "Erreur : La quantité commandée pour le produit {} est supérieure au stock disponible.".format(produit.id)


            # Perform the multiplication
            prix_total_produit = p_quantite * prix_unitaire
            prix_total = prix_total_produit + prix_total


            # Create the order line
            LigneCommande.objects.create(
                produit=produit,
                commande=commande,
                Qte=p_quantite
            )

            # Mettre à jour les niveaux de stock des produits commandés
            produit.Quantite_enStock = produit.Quantite_enStock - p_quantite
            produit.save()


        commande.prix_total = prix_total
        commande.save()      


        # Vérifier si le solde de la carte est suffisant 
        if (carte.balance<prix_total): 
            return "Erreur :Solde de la carte insuffisant pour passer la commande.. " 

        carte.balance = carte.balance - prix_total
        carte.save()

        serialized_commande = serialize('json', [commande])
        commande_json = json.loads(serialized_commande)[0]['fields']

        return commande_json
    except Exception as e:
        print("An error occurred on line:", traceback.extract_tb(sys.exc_info()[-1])[0][1])
        raise e



@calculate_execution_time
def create_commande_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Extract parameters from the request
        p_nom_client = data.get('nom_client')
        p_prenom_client = data.get('prenom_client')
        p_num_tel = data.get('num_tel')
        p_numero_carte = data.get('numero_carte')
        p_cvv = data.get('cvv')
        p_date_exp = data.get('date_exp')
        p_balance = data.get('balance')
        p_type_id = data.get('type_id')
        p_adresse = data.get('adresse')
        p_code_postal = data.get('code_postal')
        list_product_qte = data.get('list_product_qte')

        # Call create_commande function
        try:
            commande_data = create_commande(p_nom_client, p_prenom_client, p_num_tel, p_numero_carte,
                                            p_cvv, p_date_exp, p_balance, p_type_id,
                                            p_adresse, p_code_postal,list_product_qte)
            return JsonResponse({'commande': commande_data}, status=201)  # Return the created order as JSON
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)  # Return error message if an exception occurs
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)  # Return error for invalid request method


@calculate_execution_time
@require_http_methods(["PUT"])
def update_command_status(request, commande_id, nouveau_statut):
   
    try:
        commande = Commande.objects.get(id=commande_id)
        client = Client.objects.get(id=commande.client.id)
        carte = Carte.objects.filter(client=client).first()

        # Perform additional actions based on the new status
        email_data = []
        if nouveau_statut == 3: # En transit
            # Send a notification email to the client
            subject = "Commande en transit"
            message = f"Votre commande #{commande.id} est en cours de livraison."

            email_data.append({'subject': subject, 'message': message})

        elif nouveau_statut == 5: # Annulée
            # Restore products to stock
            ligne_commandes = commande.lignecommande_set.all()
            for ligne in ligne_commandes:
                ligne.produit.Quantite_enStock += ligne.Qte
                ligne.produit.save()

        elif nouveau_statut == 6: # En attente de stock
            # Send a notification email to the client
            subject = "Commande en attente de stock"
            message = f"Votre commande #{commande.id} est en attente de disponibilité des produits en stock."
            email_data.append({'subject': subject, 'message': message})

        elif nouveau_statut == 8: # Retardée
            # Send a notification email to the client
            subject = "Commande retardée"
            message = f"Votre commande #{commande.id} a été retardée pour des raisons logistiques."
            email_data.append({'subject': subject, 'message': message})

        elif nouveau_statut == 9: # Remboursée
            # Credit the client's account
            carte.balance += commande.prix_total
            carte.save()

        # Update the status of the order
        commande.status = nouveau_statut
        commande.save()


        return JsonResponse({'success': True, 'message': f"Statut de la commande {commande_id} mis à jour avec succès.", 'email_data': email_data})

    except Commande.DoesNotExist:
        return JsonResponse({'success': False, 'message': f"La commande avec l'ID {commande_id} n'existe pas."})
    except Exception as e:
        print("An error occurred on line:", traceback.extract_tb(sys.exc_info()[-1])[0][1])
        return JsonResponse({'success': False, 'message': str(e)})
    
@calculate_execution_time
def list_commands(request):
    if request.method == 'GET':
        # Retrieve all commands
        commands = Commande.objects.all()

        # Serialize commands data
        commands_data = []
        for command in commands:
            command_data = {
                'commande_date': command.commande_date,
                'status': command.status,
                'prix_total': command.prix_total,
                'client': {
                    'id': command.client.id,
                    'nom_client': command.client.nom_client,
                },
                'adresse': {
                    'id': command.adresse.id,
                    'distinaire': command.adresse.distinaire,
                }
            }
            commands_data.append(command_data)

        return JsonResponse({'commands': commands_data}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@calculate_execution_time
def list_stocks(request):
    if request.method == 'GET':

        # Retrieve all products
        products = Produit.objects.all()

        # Serialize products data
        products_data = []
        for product in products:
            product_data = {
                'code_produit': product.code_produit,
                'nom_produit': product.nom_produit,
                'Quantite_enStock': product.Quantite_enStock,
                'prix_unitaire': product.prix_unitaire,
                'description': product.description
            }
            products_data.append(product_data)

        return JsonResponse({'stocks': products_data}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

@calculate_execution_time
def alert_quantite(request):
    if request.method == 'GET':
        try:
            low_stock_products = []
            for produit in Produit.objects.all():
                quantite_en_stock = produit.Quantite_enStock
                if quantite_en_stock < 25:
                    low_stock_products.append({
                        'nom_produit': produit.nom_produit,
                        'quantite_en_stock': quantite_en_stock
                    })

            if low_stock_products:
                error_messages = []
                for product in low_stock_products:
                    error_messages.append(f"Quantité en stock du produit '{product['nom_produit']}' est très basse ({product['quantite_en_stock']})")
                return JsonResponse({'error': '\n'.join(error_messages)}, status=200)
            else:
                return JsonResponse({'message': 'No low stock alerts'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    