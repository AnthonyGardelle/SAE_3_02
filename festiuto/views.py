"""Module pour les vues de l'application."""
from flask import render_template, redirect, url_for
from flask_login import login_user, current_user, logout_user
from .app import app
from .form import SearchForm, LoginForm
from .models import get_favoris_by_spec, get_random_groupes

@app.route('/')
def home() :
    """Fonction de la vue de la page d'accueil.

    Returns:
        flask.reponse: Réponse de la page d'accueil.
    """
    if current_user.is_authenticated :
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

@app.route("/search", methods =("POST",))
def search() :
    """Fonction de la vue de la page de recherche.

    Returns:
        flask.reponse: Réponse de la page de recherche.
    """
    form = SearchForm()
    content_searched = form.searched.data
    if content_searched == "":
        return home()
    return render_template (
        "search.html",
        form=form,
        searched = content_searched,
        title = "Search Page",
    )

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
    return render_template (
        "groupe.html",
        id_group = id_group,
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
