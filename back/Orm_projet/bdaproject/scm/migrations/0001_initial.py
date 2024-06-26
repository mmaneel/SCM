# Generated by Django 5.0.6 on 2024-05-11 23:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distinaire', models.CharField(max_length=255)),
                ('code_postal', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Carte',
            fields=[
                ('numero', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('cvv', models.IntegerField()),
                ('date_exp', models.IntegerField()),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_produit', models.IntegerField()),
                ('nom_produit', models.CharField(max_length=255)),
                ('Quantite_enStock', models.IntegerField()),
                ('prix_unitaire', models.FloatField()),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TypeCarte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_client', models.CharField(max_length=255)),
                ('prenom_client', models.CharField(max_length=255)),
                ('num_tel', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('carte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm.carte')),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commande_date', models.DateField()),
                ('status', models.IntegerField()),
                ('prix_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('adresse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm.address')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm.client')),
            ],
        ),
        migrations.CreateModel(
            name='LigneCommande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Qte', models.IntegerField()),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm.commande')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm.produit')),
            ],
        ),
        migrations.AddField(
            model_name='carte',
            name='type_carte',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm.typecarte'),
        ),
    ]
