from django.utils import timezone
from django.db import transaction
from .models import *
from django.core.serializers import serialize
import json
from django.http import JsonResponse
import time
from .decorators import calculate_execution_time




def create_commande(p_nom_client, p_prenom_client, p_num_tel, p_numero_carte, p_cvv, p_date_exp, p_balance, p_type_id, p_adresse, p_code_postal, p_produit_id, p_quantite):
    try:
        # Check if the client already exists
        client, created = Client.objects.get_or_create(
            nom_client=p_nom_client,
            prenom_client=p_prenom_client,
            num_tel=p_num_tel,
            defaults={'carte_id': p_numero_carte}
        )
        if created:
            carte, _ = Carte.objects.get_or_create(
                numero=p_numero_carte,
                defaults={'cvv': p_cvv, 'date_exp': p_date_exp, 'balance': p_balance, 'type_carte_id': p_type_id}
            )
            client.carte = carte
            client.save() 

        # Check if the address already exists
        adresse, _ = Address.objects.get_or_create(
            distinaire=p_adresse,
            code_postal=p_code_postal
        )

        # Retrieve product details
        produit = Produit.objects.get(id=p_produit_id)
        prix_unitaire = produit.prix_unitaire

        # Convert string inputs to numeric types
        p_quantite = int(p_quantite)
        prix_unitaire = float(prix_unitaire)

        # Perform the multiplication
        prix_total = p_quantite * prix_unitaire

        # Create a new order
        commande = Commande.objects.create(
            commande_date=timezone.now(),
            status=0,  # Assuming initial status is 1
            prix_total=prix_total,
            client=client,
            adresse=adresse
        )


        # Create the order line
        LigneCommande.objects.create(
            produit=produit,
            commande=commande,
            Qte=p_quantite
        )

        # Update product stock levels
        produit.Quantite_enStock -= p_quantite
        produit.save()

        serialized_commande = serialize('json', [commande])
        commande_json = json.loads(serialized_commande)[0]['fields']

        return commande_json
    except Exception as e:
        # Rollback the transaction in case of any error
        transaction.set_rollback(True)
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
        p_produit_id = data.get('produit_id')
        p_quantite = data.get('quantite')

        # Call create_commande function
        try:
            commande_data = create_commande(p_nom_client, p_prenom_client, p_num_tel, p_numero_carte,
                                            p_cvv, p_date_exp, p_balance, p_type_id,
                                            p_adresse, p_code_postal, p_produit_id, p_quantite)
            return JsonResponse({'commande': commande_data}, status=201)  # Return the created order as JSON
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)  # Return error message if an exception occurs
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)  # Return error for invalid request method



@calculate_execution_time
def validate_commande(request, commande_id):
    try:
        # Retrieve the command object
        commande = Commande.objects.get(id=commande_id)

        # Get all lines of the command
        lignes_commande = LigneCommande.objects.filter(commande=commande)

        # Iterate over each line and check product availability
        for ligne_commande in lignes_commande:
            produit = ligne_commande.produit
            quantity = ligne_commande.Qte

            # Check if the product is in stock
            if produit.Quantite_enStock < quantity:
                return JsonResponse({'success': False, 'message': f'Product {produit.nom_produit} is out of stock.'}, status=400)

        # If all products are available, return success
        return JsonResponse({'success': True, 'message': 'Commande is valid.'})
    except Commande.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Commande does not exist.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    

@calculate_execution_time
@transaction.atomic
def update_command_status(request, commande_id, nouveau_statut):
    try:
        commande = Commande.objects.select_related('client', 'client__carte').get(id=commande_id)

        # Update the status of the order
        commande.status = nouveau_statut
        commande.save()

        # Perform additional actions based on the new status
        email_data = []
        if nouveau_statut == 1: # Créée
            # Send an email confirmation to the client
            subject = "Confirmation de commande"
            message = f"Votre commande #{commande.id} a été créée avec succès."
            recipient = commande.client.email
            print(subject, message, recipient)
            email_data.append({'subject': subject, 'message': message, 'recipient': recipient})

        elif nouveau_statut == 2: # Prête pour l'expédition
            # Reserve products in stock for this order
            ligne_commandes = commande.lignecommande_set.all()
            for ligne in ligne_commandes:
                ligne.produit.Quantite_enStock -= ligne.Qte
                ligne.produit.save()

        elif nouveau_statut == 3: # En transit
            # Send a notification email to the client
            subject = "Commande en transit"
            message = f"Votre commande #{commande.id} est en cours de livraison."
            recipient = commande.client.email
            print(subject, message, recipient)
            email_data.append({'subject': subject, 'message': message, 'recipient': recipient})

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
            recipient = commande.client.email
            print(subject, message, recipient)
            email_data.append({'subject': subject, 'message': message, 'recipient': recipient})

        elif nouveau_statut == 8: # Retardée
            # Send a notification email to the client
            subject = "Commande retardée"
            message = f"Votre commande #{commande.id} a été retardée pour des raisons logistiques."
            recipient = commande.client.email
            print(subject, message, recipient)
            email_data.append({'subject': subject, 'message': message, 'recipient': recipient})

        elif nouveau_statut == 9: # Remboursée
            # Credit the client's account
            carte = commande.client.carte
            carte.balance += commande.prix_total
            carte.save()

        return JsonResponse({'success': True, 'message': f"Statut de la commande {commande_id} mis à jour avec succès.", 'email_data': email_data})

    except Commande.DoesNotExist:
        return JsonResponse({'success': False, 'message': f"La commande avec l'ID {commande_id} n'existe pas."})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    

@calculate_execution_time
def check_stock_quantity(request):
    try:
        low_stock_products = Produit.objects.filter(Quantite_enStock__lt=25)

        if low_stock_products.exists():
            message = "Les produits suivants ont une quantité en stock très basse : "
            message += ", ".join([produit.nom_produit for produit in low_stock_products])
            return JsonResponse({'success': True, 'message': message})
        else:
            return JsonResponse({'success': True, 'message': "Tous les produits ont une quantité en stock suffisante."})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
