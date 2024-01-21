"""Module de la vue de l'application."""

from flask import render_template, redirect, url_for, request
from flask_login import login_user, current_user, logout_user
from .app import app
from .models import (
    Groupe,
    loger,
    get_groupes,
    get_group,
    get_favoris_by_spec,
    get_activite_by_id,
    get_random_groupes,
    get_spect_by_id,
    get_types_billets,
    get_jours_festival,
    get_duree_fest,
    get_billet,
    add_billet,
    get_hebergement,
    get_hebergement_by_id,
    inscrire,
    desinscrire,
    assiste,
    get_concert_by_id,
    enlever_assiste
)
from .form import SearchForm, LoginForm

@app.route('/')
def home() :
    """Fonction de la vue de la page d'accueil.

    Returns:
        flask.reponse: Réponse de la page d'accueil.
    """
    if current_user.is_authenticated and len(get_favoris_by_spec(current_user.id_spectateur)) > 0 :
        les_favoris = get_favoris_by_spec(current_user.id_spectateur)
        random = False
    else :
        les_favoris = get_random_groupes()
        random = True
    return render_template (
        "home.html",
        favoris = les_favoris,
        random = random
    )

@app.route("/search/", methods = ("POST",))
def search() :
    """Fonction de recherche."""
    form = SearchForm()
    groupes = get_groupes()
    if form.validate_on_submit() :
        form.searched = form.searched.data
        groupes = Groupe.query.filter(Groupe.nom_groupe.like("%" + form.searched + "%"))
        return render_template(
            "search.html",
            form=form,
            search=form.searched,
            groupes=groupes
        )
    return redirect(url_for("home"))

@app.route("/sinscrire/<int:id_activite>", methods = ("GET",))
def sinscrire_activite(id_activite) :
    """Fonction de la vue de la page d'inscription à une activité.

    Args:
        id_activite (int): Identifiant de l'activité.

    Returns:
        flask.reponse: Réponse de la page d'inscription à une activité.
    """
    activite = get_activite_by_id(id_activite)
    return render_template (
        "sinscrire_activite.html",
        activite = activite,
    )

@app.route("/sincrire-concert/<int:id_concert>", methods = ("GET",))
def sinscrire_concert(id_concert) :
    """Fonction de la vue de la page d'inscription à un concert.

    Args:
        id_concert (int): Identifiant du concert.

    Returns:
        flask.reponse: Réponse de la page d'inscription à un concert.
    """
    concert = get_concert_by_id(id_concert)
    return render_template (
        "sinscrire_concert.html",
        concert = concert,
    )

@app.route("/inscription_concert/<int:id_concert>/<int:id_spectateur>", methods = ("GET","POST"))
def bouton_sinscrire_concert(id_concert, id_spectateur) :
    """Fonction de la vue de la page de confirmation d'inscription à un concert.

    Returns:
        flask.reponse: Réponse de la page de confirmation d'inscription à un concert.
    """
    assiste(id_spectateur, id_concert)
    return redirect(url_for("home"))

@app.route("/desinscription_concert/<int:id_concert>/<int:id_spectateur>", methods = ("GET","POST"))
def bouton_desinscrire_concert(id_concert, id_spectateur) :
    """Fonction de la vue de la page de confirmation de désinscription à un concert.

    Returns:
        flask.reponse: Réponse de la page de confirmation de désinscription à un concert.
    """
    enlever_assiste(id_spectateur, id_concert)
    return redirect(url_for("home"))

@app.route("/process_inscription/<int:id_activite>/<int:id_spectateur>", methods = ("GET","POST"))
def bouton_sinscrire(id_activite, id_spectateur) :
    """Fonction de la vue de la page de confirmation d'inscription à une activité.

    Returns:
        flask.reponse: Réponse de la page de confirmation d'inscription à une activité.
    """
    inscrire(id_spectateur, id_activite)
    return redirect(url_for("home"))

@app.route("/desinscription/<int:id_activite>/<int:id_spectateur>", methods = ("GET","POST"))
def bouton_desinscrire(id_activite, id_spectateur) :
    """Fonction de la vue de la page de confirmation de désinscription à une activité.

    Returns:
        flask.reponse: Réponse de la page de confirmation de désinscription à une activité.
    """
    desinscrire(id_spectateur, id_activite)
    return redirect(url_for("home"))

@app.context_processor
def base() :
    """Fonction de la vue pour le formulaire de recherche.

    Returns:
        flask.reponse: Réponse du formulaire de recherche.
    """
    form = SearchForm()
    return {"form": form}

@app.route("/billeterie")
def billeterie() :
    """Fonction de la vue de la page de la billeterie.

    Returns:
        flask.reponse: Réponse de la page de la billeterie.
    """
    types_billet = get_types_billets()
    jours_festival = get_jours_festival()
    duree_fest = get_duree_fest()
    return render_template("billeterie.html",
                        types_billet = types_billet,
                        dates = jours_festival,
                        duree_fest = duree_fest)

@app.route("/resume_reservation", methods=["POST"])
def resume_reservation() :
    """Fonction de la vue de la page de confirmation de réservation.

    Returns:
        flask.reponse: Réponse de la page de confirmation de réservation.
    """
    data = request.form
    ind_type_billet = int(data["type_billet_id"])
    date_debut = data["date_debut"]

    spect = get_spect_by_id(current_user.id_spectateur)
    spectateur = spect.to_dict()

    billet_ajoute = add_billet(current_user.id_spectateur, 1, ind_type_billet, date_debut)

    if not billet_ajoute:
        error_message = "Erreur : Ce billet existe déjà"
        print("Erreur : Ce billet existe déjà")
        return render_template("resume_reservation.html",
                            error_message = error_message,
                            redirect_url = "/billeterie")

    billet = get_billet(current_user.id_spectateur, 1, ind_type_billet, date_debut).to_dict()
    return render_template("resume_reservation.html", billet=billet, spectateur=spectateur)

@app.route("/process_inscription", methods=["POST"])
def process_inscription() :
    """Fonction de la vue de la page de confirmation d'inscription à une activité.

    Returns:
        flask.reponse: Réponse de la page de confirmation d'inscription à une activité.
    """
    data = request.form
    print(data)
    error_message = "Merci pour votre inscription !"
    concert_ids = data.getlist('concert_ids[]')
    id_spectateur = data["spectateur_id"]
    for concert_id in concert_ids:
        print(assiste(id_spectateur, concert_id))
    return render_template("resume_reservation.html",
                        error_message = error_message,
                        redirect_url = url_for('home'))


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
    legroupe = get_group(id_group)
    taille = len(legroupe.get_membres())
    return render_template (
        "groupe.html",
        groupe = legroupe,
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
    spectateur = get_spect_by_id(id_spectateur)
    return render_template (
        "profil.html",
        spectateur = spectateur,
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
    return redirect(url_for("login"))

@app.route("/admin")
def admin() :
    """Fonction de la vue de la page d'administration.

    Returns:
        flask.reponse: Réponse de la page d'administration.
    """
    liste_groupe = []
    for ungroupe in Groupe.query.all():
        grp = ungroupe.to_dict()
        liste_groupe.append(grp)
    hebergements = get_hebergement()
    list_hebergements = []
    for hebergement in hebergements:
        heb = hebergement.to_dict()
        list_hebergements.append(heb)
    return render_template("admin.html", groupes = liste_groupe, hebergements = list_hebergements)

@app.route("/process_hebergement", methods=["POST"])
def process_hebergement() :
    """Fonction pour loger un groupe dans un hébergement.

    Returns:
        flask.reponse: Réponse de la page de confirmation de logement.
    """
    data = request.form
    print(data)
    id_hebergement = data["hebergement"]
    id_groupe = data["groupe.id"]
    print(loger(id_groupe, id_hebergement))
    nom_groupe = get_group(id_groupe).nom_groupe
    nom_hebergement = get_hebergement_by_id(id_hebergement).nom_hebergement
    error_message = f"Le groupe {nom_groupe} a été logé dans l'hébergement {nom_hebergement}"
    return render_template("resume_reservation.html",
                        error_message = error_message,
                        redirect_url = url_for('admin'))

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

@app.route("/programme", methods = ("GET",))
def programme() :
    """Fonction de la vue de la page du programme.

    Returns:
        flask.reponse: Réponse de la page du programme.
    """
    les_groupes = get_groupes()
    return render_template (
        "programme.html",
        groupes = les_groupes
    )
