from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Commande

@receiver(post_save, sender=Commande)
def track_order_status(sender, instance, created, **kwargs):
    if not created:
        status_choices = {
            1: 'Créée',
            2: 'Prête pour l\'expédition',
            3: 'En transit',
            4: 'Livraison réussie',
            5: 'Annulée',
            6: 'En attente de stock',
            7: 'En attente de confirmation',
            8: 'Retardée',
            9: 'Remboursée',
        }
        status = status_choices.get(instance.status, 'Statut inconnu')
        print(f"Suivi en temps réel de la commande {instance.id}: {status}")
