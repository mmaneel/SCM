from django.urls import path
from . import views

urlpatterns = [
    path('create-commande/', views.create_commande_view, name='create-commande'),
    path('validate-commande/<int:commande_id>/', views.validate_commande, name='validate_commande'),
    path('update-command-status/<int:commande_id>/<int:nouveau_statut>/', views.update_command_status, name='update_command_status'),
    path('check-stock-quantity/', views.check_stock_quantity, name='check_stock_quantity'),
   
]
