"""Module pour la création de la base de données et l'import des données."""

import csv
import os
import click
from .app import app,db
from .models import (ajouter_festival,
                    ajouter_lieu,
                    ajouter_festival_lieu,
                    ajouter_type_billet,
                    ajouter_genre_musical,
                    ajouter_groupe,
                    ajouter_spectateur,
                    ajouter_favoris,
                    ajouter_photos,
                    ajouter_se_produire,
                    ajouter_concert,
                    ajouter_artiste,
                    ajouter_reseaux_sociaux,
                    ajouter_hebergement,
                    ajouter_activite,
                    participe,
                    ajouter_organise,
                    Spectateur)

@app.cli.command()
@click.argument('dirname')
def loaddb(dirname):
    '''Creates the tables and populates them with data.'''
    db.drop_all()
    db.create_all()
    for nom_fichier in os.listdir(dirname):
        chemin_fichier = os.path.join(dirname, nom_fichier)
        if os.path.isfile(chemin_fichier) and nom_fichier.endswith('.csv'):
            print("\033[92m" + f"Traitement du fichier CSV {nom_fichier} :" + "\033[0m")
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
                            nom = row['nom_lieu']
                            adresse = row['adresse_lieu']
                            ville = row['ville_lieu']
                            postal = row['code_postal_lieu']
                            pays = row['pays_lieu']
                            capacite = row['capacite_lieu']
                            type_l = row['type_lieu']
                            print(ajouter_lieu(nom, adresse, ville, postal, pays, capacite, type_l))
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
                            nom = row["nom_groupe"]
                            id_groupe = row["id_genre_musical"]
                            date_a = row["date_arrivee"]
                            date_d = row["date_depart"]
                            heure_a = row["heure_arrivee"]
                            heure_d = row["heure_depart"]
                            print(ajouter_groupe(nom, id_groupe, date_a, date_d, heure_a, heure_d))
                elif nom_table == "spectateur" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            id_spectateur = row["id_spectateur"]
                            nom = row["nom_spectateur"]
                            prenom = row["prenom_spectateur"]
                            mdp = row["mot_de_passe_spectateur"]
                            print(ajouter_spectateur(nom, prenom, mdp))
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
                            id_group = row["id_groupe"]
                            id_concert = row["id_concert"]
                            print(ajouter_se_produire(id_group, id_concert))
                elif nom_table == "lzconcert":
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            nom = row["nom_concert"]
                            date = row["date_concert"]
                            heur = row["heure_debut_concert"]
                            duree = row["duree_concert"]
                            mtge = row["temps_montage"]
                            detge = row["temps_demontage"]
                            lieu = row["id_lieu"]
                            genre = row["id_genre_musical"]
                            print(ajouter_concert(nom, date, heur, duree, mtge, detge, lieu, genre))
                elif nom_table == "artiste" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            nom = row["nom_artiste"]
                            prenom = row["prenom_artiste"]
                            instrument = row["instrument_artiste"]
                            id_groupe = row["id_groupe"]
                            print(ajouter_artiste(nom, prenom, instrument, id_groupe))
                elif nom_table == "reseaux_sociaux" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            nom = row["nom_reseaux_sociaux"]
                            url = row["url_reseaux_sociaux"]
                            id_group = row["id_group"]
                            print(ajouter_reseaux_sociaux(nom, url, id_group))
                elif nom_table == "hebergement" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            nom = row["nom_hebergement"]
                            adresse = row["adresse_hebergement"]
                            ville = row["ville_hebergement"]
                            code_postal = row["code_postal_hebergement"]
                            capacite = row["capacite_hebergement"]
                            print(ajouter_hebergement(nom, adresse, ville, code_postal, capacite))
                elif nom_table == "activite" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            nom = row["nom_activite"]
                            statut = row["statut_publique"]
                            date = row["date_activite"]
                            heure_d = row["heure_debut_activite"]
                            duree = row["duree_activite"]
                            print(ajouter_activite(nom, statut, date, heure_d, duree))
                elif nom_table == "participer" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            id_groupe = row["id_groupe"]
                            id_activite = row["id_activite"]
                            print(participe(id_groupe, id_activite))
                elif nom_table == "organise" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            id_activite = row["id_activite"]
                            id_lieu = row["id_lieu"]
                            print(ajouter_organise(id_activite, id_lieu))
                else:
                    print("\033[91m" + f"Erreur : table {nom_table} non reconnue." + "\033[0m")
            except InterruptedError as e:
                print(f"Erreur : {e}")
                db.session.rollback()
            else:
                db.session.commit()
                print(f"Table {nom_table} importée avec succès.")
    print("Import terminé.")
    new_admin(['adminP', 'adminN', 'admin']) #pylint: disable = no-value-for-parameter

@app.cli.command()
@click.argument('nom_admin')
@click.argument('prenom_admin')
@click.argument('mot_de_passe_admin')
def new_admin(nom_admin, prenom_admin, mot_de_passe_admin):
    '''Creates the admin account.'''
    admin = Spectateur(nom_admin, prenom_admin, mot_de_passe_admin)
    admin.admin = True
    db.session.add(admin)
    db.session.commit()
    print("Admin créé avec succès.")
    promote(['1'])

@app.cli.command()
@click.argument('id_spect')
def promote(id_spect):
    '''Promotes a user to admin.'''
    spect = Spectateur.query.get(id_spect)
    spect.admin = True
    db.session.commit()
    print("Utilisateur promu avec succès.")

app.cli.add_command(new_admin)
app.cli.add_command(promote)
