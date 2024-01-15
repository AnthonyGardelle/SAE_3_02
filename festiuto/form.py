"""Module contenant les classes formulaires de l'application."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm) :
    """Classe formulaire de recherche.

    Args:
        FlaskForm (class): Classe formulaire de Flask.
    """
    searched = StringField('Searched', validators=[DataRequired()])
    submit = SubmitField("Submit", validators=[DataRequired()])
