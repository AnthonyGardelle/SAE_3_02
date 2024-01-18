from flask import flash, redirect, render_template, request, url_for
from .app import app
from .form import SearchForm
from .models import *

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/search", methods=("POST",))
def search():
    form = SearchForm()
    content_searched = form.searched.data
    if content_searched == "":
        return home()
    return render_template("search.html", form=form, searched=content_searched, title="Search Page")

@app.route("/billeterie")
def billeterie():
    types_billet = get_types_billets()
    jours_festival = get_jours_festival()
    duree_fest = get_duree_fest()
    return render_template("billeterie.html", types_billet=types_billet, dates=jours_festival, duree_fest=duree_fest)

@app.route("/resume_reservation", methods=["POST"])
def resume_reservation():
    data = request.form
    ind_type_billet = int(data["type_billet_id"])
    nom = data["nom"]
    prenom = data["prenom"]
    mail = data["mail"]
    date_debut = data["date_debut"]

    spect = get_spectateur(nom, prenom)
    if spect is None:
        print(add_spectateur(nom, prenom))
        spect = get_spectateur(nom, prenom)
    spectateur = spect.to_dict()
    id_spect = spectateur["id"]

    billet_ajoute = add_billet(id_spect, 1, ind_type_billet, date_debut)

    if not billet_ajoute:
        error_message = "Erreur : Ce billet existe déjà"    
        print("Erreur : Ce billet existe déjà")
        return render_template("resume_reservation.html", error_message=error_message, redirect_url="/billeterie")

    billet = get_billet(id_spect, 1, ind_type_billet, date_debut).to_dict()
    return render_template("resume_reservation.html", billet=billet, spectateur=spectateur)