from .app import app
from .models import *
from flask import render_template, redirect, url_for, request
from flask_login import login_user, current_user, logout_user
from .form import SearchForm, LoginForm

@app.route('/')
def home() :
    """Fonction de la vue de la page d'accueil.

    Returns:
        flask.reponse: Réponse de la page d'accueil.
    """
    if current_user.is_authenticated and len(get_favoris_by_spec(current_user.id_spectateur)) > 0 :
        favoris = get_favoris_by_spec(current_user.id_spectateur)
        random = False
    else :
        favoris = get_random_groupes()
        random = True
    print(favoris)
    print(random)
    return render_template (
        "home.html",
        favoris = favoris,
        random = random
    )

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

    spect = get_spect_by_id(current_user.id_spectateur)
    spectateur = spect.to_dict()

    billet_ajoute = add_billet(current_user.id_spectateur, 1, ind_type_billet, date_debut)

    if not billet_ajoute:
        error_message = "Erreur : Ce billet existe déjà"    
        print("Erreur : Ce billet existe déjà")
        return render_template("resume_reservation.html", error_message=error_message, redirect_url="/billeterie")

    billet = get_billet(current_user.id_spectateur, 1, ind_type_billet, date_debut).to_dict()
    return render_template("resume_reservation.html", billet=billet, spectateur=spectateur)

@app.route("/process_inscription", methods=["POST"])
def process_inscription():
    data = request.form
    print(data)
    error_message = "Merci pour votre inscription !"
    concert_ids = data.getlist('concert_ids[]')
    id_spectateur = data["spectateur_id"]
    for id in concert_ids:
        print(assiste(id_spectateur, id))
    return render_template("resume_reservation.html", error_message=error_message, redirect_url=url_for('home'))


@app.route("/login/", methods = ("GET", "POST"))
def login() :
    """Fonction de la vue de la page de connexion.

    Returns:
        flask.reponse: Réponse de la page de connexion.
    """
    form = LoginForm()
    if form.validate_on_submit() :
        user = form.get_authenticated_user()
        if user :
            login_user(user)
            return redirect(url_for("home"))
    return render_template (
        "login.html",
        form=form,
    )

@app.route("/group/<int:id_group>", methods = ("GET",))
def groupe(id_group) :
    """Fonction de la vue de la page d'un groupe.

    Args:
        id_group (int): Identifiant du groupe.

    Returns:
        flask.reponse: Réponse de la page du groupe.
    """
    groupe = get_group(id_group)
    taille = len(groupe.get_membres())
    return render_template (
        "groupe.html",
        groupe = groupe,
        taille = taille
    )

@app.route("/profil/<int:id_spectateur>", methods = ("GET",))
def profil(id_spectateur) :
    """Fonction de la vue de la page d'un profil.

    Args:
        id_spectateur (int): Identifiant du spectateur.

    Returns:
        flask.reponse: Réponse de la page du profil.
    """
    return render_template (
        "profil.html",
        id_spectateur = id_spectateur,
    )

@app.route("/deconnexion/", methods = ("GET",))
def deconnexion() :
    """Fonction de la vue de la page de déconnexion.

    Returns:
        flask.reponse: Réponse de la page de déconnexion.
    """
    logout_user()
    return redirect(url_for("home"))

@app.route("/suivre/<int:id_group>", methods = ("GET",))
def suivre(id_group) :
    """Fonction de la vue de la page de suivi d'un groupe.

    Args:
        id_group (int): Identifiant du groupe.

    Returns:
        flask.reponse: Réponse de la page de suivi d'un groupe.
    """
    if current_user.is_authenticated :
        current_user.ajouter_favoris(id_group)
        return redirect(url_for("groupe", id_group=id_group))
    else :
        return redirect(url_for("login"))
    
@app.route("/unsuivre/<int:id_group>", methods = ("GET",))
def unsuivre(id_group) :
    """Fonction de la vue de la page de désuivi d'un groupe.

    Args:
        id_group (int): Identifiant du groupe.

    Returns:
        flask.reponse: Réponse de la page de désuivi d'un groupe.
    """
    if current_user.is_authenticated :
        current_user.enlever_favoris(id_group)
        print("unsuivre")
        return redirect(url_for("groupe", id_group=id_group))
    else :
        return redirect(url_for("login"))

@app.route("/favoris", methods = ("GET",))
def favoris() :
    """Fonction de la vue de la page des favoris.

    Returns:
        flask.reponse: Réponse de la page des favoris.
    """
    les_favoris = get_favoris_by_spec(current_user.id_spectateur)
    return render_template (
        "favoris.html",
        favoris = les_favoris
    )