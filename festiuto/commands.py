import csv
import os
import click
from .app import app,db
from .models import *

@app.cli.command()
@click.argument('dirname')
def loaddb(dirname):
    '''Creates the tables and populates them with data.'''
    db.drop_all()
    # Create tables 
    db.create_all()

    chemin_dossier = ""

    # Parcours de tous les fichiers du dossier
    for nom_fichier in os.listdir(dirname):
        chemin_fichier = os.path.join(dirname, nom_fichier)
        if os.path.isdir(chemin_fichier):
            chemin_dossier = chemin_fichier
        if os.path.isfile(chemin_fichier) and nom_fichier.endswith('.csv'):
            print(f"Traitement du fichier CSV {nom_fichier} :")
            nom_table = os.path.splitext(nom_fichier)[0]
            try:
                if nom_table == "festival":
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            id_fest = row['id_fest']
                            nom = row['nom']
                            date_debut = row['date_debut']
                            duree = row['duree']
                            print(ajouter_festival(id_fest, nom, date_debut, duree))
                elif nom_table == "lieu":
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            nom_lieu = row['nom_lieu']
                            adresse_lieu = row['adresse_lieu']
                            ville_lieu = row['ville_lieu']
                            code_postal_lieu = row['code_postal_lieu']
                            pays_lieu = row['pays_lieu']
                            capacite_lieu = row['capacite_lieu']
                            type_lieu = row['type_lieu']
                            print(ajouter_lieu(nom_lieu, adresse_lieu, ville_lieu, code_postal_lieu, pays_lieu, capacite_lieu, type_lieu))
                elif nom_table == "festival_lieu":
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:  
                            id_fest = row['id_fest']
                            id_lieu = row['id_lieu']
                            print(ajouter_festival_lieu(id_fest, id_lieu))
                elif nom_table == "type_billet":
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            nom = row['nom_type_billet']
                            validite = row['duree_validite_type_billet']
                            prix = row['prix_type_billet']
                            quantite_dispo = row['quantite_initiale_disponible_type_billet']
                            print(ajouter_type_billet(nom, validite, prix, quantite_dispo))
                elif nom_table == "genre_musical" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            nom_genre_musical = row['nom_genre_musical']
                            print(ajouter_genre_musical(nom_genre_musical))
                elif nom_table == "groupe" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            nom_groupe = row["nom_groupe"]
                            id_genre_musical = row["id_genre_musical"]
                            print(ajouter_groupe(nom_groupe, id_genre_musical))
                elif nom_table == "spectateur" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            id_spectateur = row["id_spectateur"]
                            nom_spectateur = row["nom_spectateur"]
                            prenom_spectateur = row["prenom_spectateur"]
                            mot_de_passe_spectateur = row["mot_de_passe_spectateur"]
                            print(ajouter_spectateur(nom_spectateur, prenom_spectateur, mot_de_passe_spectateur))
                elif nom_table == "favoris" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            id_group = row["id_group"]
                            id_spectateur = row["id_spectateur"]
                            print(ajouter_favoris(id_group, id_spectateur))
                elif nom_table == "photos" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            url_photo = row["url_photo"]
                            id_group = row["id_group"]
                            print(ajouter_photos(url_photo, id_group))
                elif nom_table == "se_produire" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:  
                            id_group = row["id_group"]
                            id_concert = row["id_concert"]
                            print(ajouter_se_produire(id_group, id_concert))
                elif nom_table == "lzconcert":
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';') 
                        for row in reader:  
                            nom_concert = row["nom_concert"]
                            date_concert = row["date_concert"]
                            heure_debut_concert = row["heure_debut_concert"]
                            duree_concert = row["duree_concert"]
                            temps_montage = row["temps_montage"]
                            temps_demontage = row["temps_demontage"]
                            id_lieu = row["id_lieu"]
                            id_genre_musical = row["id_genre_musical"]
                            print(ajouter_concert(nom_concert, date_concert, heure_debut_concert, duree_concert, temps_montage, temps_demontage, id_lieu, id_genre_musical))
                else:
                    print(f"Erreur : table {nom_table} non reconnue.")
            except Exception as e:
                print(f"Erreur : {e}")
                db.session.rollback()
            else:
                db.session.commit()
                print(f"Table {nom_table} importée avec succès.")
    print("Import terminé.")