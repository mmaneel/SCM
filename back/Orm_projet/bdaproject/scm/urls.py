from django.urls import path
from . import views

urlpatterns = [
    path('create-commande/', views.create_commande_view, name='create-commande'),
    path('update-command-status/<int:commande_id>/<int:nouveau_statut>/', views.update_command_status, name='update_command_status'),
    path('list_commands/', views.list_commands, name='list_commands'),
    path('list_stocks/', views.list_stocks, name='list_stocks'),
    path('alert-quantite/', views.alert_quantite, name='alert_quantite'),
   
]
