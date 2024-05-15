from django.db import models

class TypeCarte(models.Model):
    nom = models.CharField(max_length=255)

class Produit(models.Model):
    code_produit = models.IntegerField()
    nom_produit = models.CharField(max_length=255)
    Quantite_enStock = models.IntegerField()
    prix_unitaire = models.FloatField()
    description = models.CharField(max_length=255)

class Address(models.Model):
    distinaire = models.CharField(max_length=255)
    code_postal = models.IntegerField()

class Client(models.Model):
    nom_client = models.CharField(max_length=255)
    prenom_client = models.CharField(max_length=255)
    num_tel = models.CharField(max_length=255)

class Carte(models.Model):
    numero = models.CharField(max_length=16, primary_key=True)
    cvv = models.IntegerField(null=False)
    date_exp = models.IntegerField(null=False)
    balance = models.DecimalField(max_digits=10, decimal_places=0)  # Adjusted precision
    type_carte = models.ForeignKey(TypeCarte, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.numero

class Commande(models.Model):
    commande_date = models.DateField()
    status = models.IntegerField()
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    adresse = models.ForeignKey(Address, on_delete=models.CASCADE)

class LigneCommande(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    Qte = models.IntegerField()

