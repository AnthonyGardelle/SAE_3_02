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
                            date_arrivee = row["date_arrivee"]
                            date_depart = row["date_depart"]
                            heure_arrivee = row["heure_arrivee"]
                            heure_depart = row["heure_depart"]
                            print(ajouter_groupe(nom_groupe, id_genre_musical, date_arrivee, date_depart, heure_arrivee, heure_depart))
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
                            id_group = row["id_groupe"]
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
                elif nom_table == "artiste" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:  
                            nom_artiste = row["nom_artiste"]
                            prenom_artiste = row["prenom_artiste"]
                            instrument_artiste = row["instrument_artiste"]
                            id_groupe = row["id_groupe"]
                            print(ajouter_artiste(nom_artiste, prenom_artiste, instrument_artiste, id_groupe))
                elif nom_table == "reseaux_sociaux" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';') 
                        for row in reader:
                            nom_reseaux_sociaux = row["nom_reseaux_sociaux"]
                            url_reseaux_sociaux = row["url_reseaux_sociaux"]
                            id_group = row["id_group"]
                            print(ajouter_reseaux_sociaux(nom_reseaux_sociaux, url_reseaux_sociaux, id_group))
                elif nom_table == "hebergement" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';') 
                        for row in reader:
                            nom_hebergement = row["nom_hebergement"]
                            adresse_hebergement = row["adresse_hebergement"]
                            ville_hebergement = row["ville_hebergement"]
                            code_postal_hebergement = row["code_postal_hebergement"]
                            capacite_hebergement = row["capacite_hebergement"]
                            print(ajouter_hebergement(nom_hebergement, adresse_hebergement, ville_hebergement, code_postal_hebergement, capacite_hebergement))
                elif nom_table == "activite" :
                    with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';') 
                        for row in reader:
                            nom_activite = row["nom_activite"]
                            statut = row["statut_publique"]
                            date_activite = row["date_activite"]
                            heure_debut_activite = row["heure_debut_activite"]
                            duree_activite = row["duree_activite"]
                            print(ajouter_Activite(nom_activite, statut, date_activite, heure_debut_activite, duree_activite))
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
            except Exception as e:
                print(f"Erreur : {e}")
                db.session.rollback()
            else:
                db.session.commit()
                print(f"Table {nom_table} importée avec succès.")
    print("Import terminé.")
    new_admin(['adminP', 'adminN', 'admin'])
    
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
