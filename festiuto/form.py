"""Module contenant les classes formulaires de l'application."""
from hashlib import sha256
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from .models import Spectateur

class SearchForm(FlaskForm) :
    """Classe formulaire de recherche.

    Args:
        FlaskForm (class): Classe formulaire de Flask.
    """
    searched = StringField('Searched', validators=[DataRequired()])
    submit = SubmitField("Submit", validators=[DataRequired()])

class LoginForm(FlaskForm) :
    """Classe formulaire de connexion.

    Args:
        FlaskForm (class): Classe formulaire de Flask.
    """
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prenom', validators=[DataRequired()])
    mot_de_passe_spectateur = PasswordField('Mot de passe', validators=[DataRequired()])

    def get_authenticated_user(self) :
        """Fonction de récupération de l'utilisateur authentifié.

        Returns:
            Spectateur: Spectateur authentifié.
        """
        user = Spectateur.query.filter_by(
            nom_spectateur = self.nom.data,
            prenom_spectateur = self.prenom.data,
            mot_de_passe_spectateur = sha256(self.mot_de_passe_spectateur.data.encode()).hexdigest()
        ).first()
        return user if user else None
