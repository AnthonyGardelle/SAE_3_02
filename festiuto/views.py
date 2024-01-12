"""Module pour les vues de l'application."""
from flask import render_template
from .app import app
from .form import SearchForm

@app.route('/')
def home() :
    """Fonction de la vue de la page d'accueil.

    Returns:
        flask.reponse: Réponse de la page d'accueil.
    """
    return render_template('home.html')

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
