"""Modèle de données."""

from hashlib import sha256
from datetime import datetime, timedelta
from sqlalchemy import CheckConstraint
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin
from .app import db, login_manager

class GenreMusical(db.Model) :
    """Classe de genre musical.

    Args:
        db (class): Classe de base de données.

    Returns:
        GenreMusical: Genre musical.
    """
    __tablename__ = 'Genre_Musical'
    id_genre_musical = db.Column(db.Integer, primary_key=True)
    nom_genre_musical = db.Column(db.String(50), nullable=False)

    def __init__(self, nom) :
        """Constructeur de genre musical.

        Args:
            nom (str): Nom du genre musical.
        """
        self.nom_genre_musical = nom

    def get_groupes(self) :
        """Fonction de récupération des groupes du genre musical.

        Returns:
            list: Liste des groupes du genre musical.
        """
        return Groupe.query.filter_by(id_genre_musical=self.id_genre_musical).all()

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire du genre musical.
        """
        return {
            'id': self.id_genre_musical,
            'nom': self.nom_genre_musical,
        }

class Lieu(db.Model) :
    """Classe de lieu.

    Args:
        db (class): Classe de base de données.

    Returns:
        Lieu: Lieu.
    """
    __tablename__ = 'Lieu'
    id_lieu = db.Column(db.Integer, primary_key=True)
    nom_lieu = db.Column(db.String(50), nullable=False)
    adresse_lieu = db.Column(db.String(50), nullable=False)
    ville_lieu = db.Column(db.String(50), nullable=False)
    code_postal_lieu = db.Column(db.String(50), nullable=False)
    pays_lieu = db.Column(db.String(50), nullable=False)
    capacite_lieu = db.Column(db.Integer, nullable=False)
    type_lieu = db.Column(db.String(50), nullable=False)

    def __init__(self, nom, adresse, ville, code_postal, pays, capacite, type_lieu) :
        """Constructeur de lieu.

        Args:
            nom (str): Nom du lieu.
            adresse (str): Adresse du lieu.
            ville (str): Ville du lieu.
            code_postal (str): Code postal du lieu.
            pays (str): Pays du lieu.
            capacite (int): Capacité du lieu.
            type_lieu (str): Type du lieu.
        """
        self.nom_lieu = nom
        self.adresse_lieu = adresse
        self.ville_lieu = ville
        self.code_postal_lieu = code_postal
        self.pays_lieu = pays
        self.capacite_lieu = capacite
        self.type_lieu = type_lieu

    def get_concerts(self) :
        """Fonction de récupération des concerts du lieu.

        Returns:
            list: Liste des concerts du lieu.
        """
        return Concert.query.filter_by(id_lieu=self.id_lieu).all()

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire du lieu.
        """
        return {
            'id': self.id_lieu,
            'nom': self.nom_lieu,
            'adresse': self.adresse_lieu,
            'ville': self.ville_lieu,
            'code_postal': self.code_postal_lieu,
            'pays': self.pays_lieu,
            'capacite': self.capacite_lieu,
            'type': self.type_lieu,
        }

class Festival(db.Model) :
    """Classe de festival.

    Args:
        db (class): Classe de base de données.

    Returns:
        Festival: Festival.
    """
    __tablename__ = 'Festival'
    id_fest = db.Column(db.Integer, primary_key=True)
    nom_fest = db.Column(db.String(50), nullable=False)
    date_debut_fest = db.Column(db.Date, nullable=False)
    duree_fest = db.Column(db.Integer, nullable=False)

    def __init__(self, id_fest, nom, date_debut, duree) :
        """Constructeur de festival.

        Args:
            id_fest (int): Identifiant du festival.
            nom (str): Nom du festival.
            date_debut (date): Date de début du festival.
            duree (int): Durée du festival.
        """
        self.id_fest = id_fest
        self.nom_fest = nom
        self.date_debut_fest = date_debut
        self.duree_fest = duree

    def get_concerts(self) :
        """Fonction de récupération des concerts du festival.

        Returns:
            list: Liste des concerts du festival.
        """
        return Concert.query.filter_by(id_fest=self.id_fest).all()

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire du festival.
        """
        return {
            'id': self.id_fest,
            'nom': self.nom_fest,
            'date_debut': self.date_debut_fest,
            'duree': self.duree_fest,
            'concerts': [concert.to_dict() for concert in Concert.query.all()],
        }

class Spectateur(db.Model, UserMixin) :
    """Classe de spectateur.

    Args:
        db (class): Classe de base de données.
        UserMixin (class): Classe de gestion des utilisateurs.

    Returns:
        Spectateur: Spectateur.
    """
    __tablename__ = 'Spectateur'
    id_spectateur = db.Column(db.Integer, primary_key=True)
    nom_spectateur = db.Column(db.String(50), nullable=False)
    prenom_spectateur = db.Column(db.String(50), nullable=False)
    mot_de_passe_spectateur = db.Column(db.String(64), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, nom, prenom, mot_de_passe) :
        """Constructeur de spectateur.

        Args:
            nom (str): Nom du spectateur.
            prenom (str): Prénom du spectateur.
            mot_de_passe (str): Mot de passe du spectateur.
        """
        self.nom_spectateur = nom
        self.prenom_spectateur = prenom
        self.mot_de_passe_spectateur = mot_de_passe

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire du spectateur.
        """
        return {
            'id': self.id_spectateur,
            'nom': self.nom_spectateur,
            'prenom': self.prenom_spectateur,
            'mot_de_passe': self.mot_de_passe_spectateur,
        }

    def get_id(self) :
        """Fonction de récupération de l'identifiant du spectateur.

        Returns:
            int: Identifiant du spectateur.
        """
        return self.id_spectateur

    def ajouter_favoris(self, id_group) :
        """Fonction d'ajout d'un groupe aux favoris du spectateur.

        Args:
            id_group (int): Identifiant du groupe.

        Returns:
            str: Message de retour.
        """
        if not id_group:
            return "L'id du groupe ne peut pas être vide"
        try :
            favoris = Favoris(id_group, self.id_spectateur)
            db.session.add(favoris)
            db.session.commit()
            return f"Le groupe {id_group} a été ajouté aux favoris du spect {self.id_spectateur}"
        except IntegrityError as e:
            db.session.rollback()
            return "Erreur : " + str(e)
        except ValueError as e:
            db.session.rollback()
            return "Erreur : " + str(e)

    def enlever_favoris(self, id_group) :
        """Fonction de suppression d'un groupe des favoris du spectateur.

        Args:
            id_group (int): Identifiant du groupe.

        Returns:
            str: Message de retour.
        """
        if not id_group:
            return "L'id du groupe ne peut pas être vide"
        try :
            favoris = get_favori(id_group, self.id_spectateur)
            db.session.delete(favoris)
            db.session.commit()
            return f"Le groupe {id_group} a été enlevé des favoris du spect {self.id_spectateur}"
        except IntegrityError as e:
            db.session.rollback()
            return "Erreur : " + str(e)
        except ValueError as e:
            db.session.rollback()
            return "Erreur : " + str(e)

class Hebergement(db.Model) :
    """Classe d'hébergement.

    Args:
        db (class): Classe de base de données.

    Returns:
        Hebergement: Hébergement.
    """
    __tablename__ = 'Hebergement'
    id_hebergement = db.Column(db.Integer, primary_key=True, autoincrement = True)
    nom_hebergement = db.Column(db.String(50), nullable=False)
    adresse_hebergement = db.Column(db.String(50), nullable=False)
    ville_hebergement = db.Column(db.String(50), nullable=False)
    code_postal_hebergement = db.Column(db.String(50), nullable=False)
    capacite_hebergement = db.Column(db.Integer, nullable=False)

    def __init__(self, nom, adresse, ville, code_postal, capacite) :
        """Fonction de construction d'un hébergement.

        Args:
            nom (str): Nom de l'hébergement.
            adresse (str): Adresse de l'hébergement.
            ville (str): Ville de l'hébergement.
            code_postal (str): Code postal de l'hébergement.
            capacite (int): Capacité de l'hébergement.
        """
        self.nom_hebergement = nom
        self.adresse_hebergement = adresse
        self.ville_hebergement = ville
        self.code_postal_hebergement = code_postal
        self.capacite_hebergement = capacite

    def get_logements(self) :
        """Fonction de récupération des logements.

        Returns:
            list: Liste des logements.
        """
        return SeLoger.query.filter_by(id_hebergement=self.id_hebergement).all()

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire de l'hébergement.
        """
        return {
            'id': self.id_hebergement,
            'nom': self.nom_hebergement,
            'adresse': self.adresse_hebergement,
            'ville': self.ville_hebergement,
            'code_postal': self.code_postal_hebergement,
            'capacite': self.capacite_hebergement,
        }

class Activite(db.Model) :
    """Classe d'activité.

    Args:
        db (class): Classe de base de données.

    Returns:
        Activite: Activité.
    """
    __tablename__ = 'Activite'
    id_activite = db.Column(db.Integer, primary_key=True, autoincrement = True)
    nom_activite = db.Column(db.String(50), nullable=False)
    statut_publique = db.Column(db.Boolean, nullable=False)
    date_activite = db.Column(db.Date, nullable=False)
    heure_debut_activite = db.Column(db.Time, nullable=False)
    duree_activite = db.Column(db.Time, nullable=False)

    def __init__(self, nom, statut, date_debut , heure_debut, duree) :
        """Fonction de construction d'une activité.

        Args:
            nom (str): Nom de l'activité.
            statut (str): Statut de l'activité.
            date_debut (date): Date de début de l'activité.
            heure_debut (time): Heure de début de l'activité.
            duree (time): Durée de l'activité.
        """
        self.nom_activite = nom
        self.statut_publique = statut
        self.date_activite = date_debut
        self.heure_debut_activite = heure_debut
        self.duree_activite = duree

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire de l'activité.
        """
        return {
            'id': self.id_activite,
            'nom': self.nom_activite,
            'statut_publique': self.statut_publique,
            'date_debut': self.date_activite,
            'heure_debut': self.heure_debut_activite,
            'duree': self.duree_activite,
        }

    def get_date_fin(self) :
        """Fonction de récupération de la date de fin de l'activité.

        Returns:
            date: Date de fin de l'activité.
        """
        debut = self.heure_debut_activite
        duree = self.duree_activite
        diff_debut = timedelta(hours=debut.hour, minutes=debut.minute, seconds=debut.second)
        diff_duree = timedelta(hours=duree.hour, minutes=duree.minute, seconds=duree.second)
        difference = diff_debut + diff_duree
        return (datetime.min + difference).time()

    def est_inscrit(self, id_spectateur) :
        """Fonction de vérification de l'inscription d'un spectateur à une activité.

        Args:
            id_spectateur (int): Identifiant du spectateur.

        Returns:
            bool: Vrai si le spectateur est inscrit à l'activité, faux sinon.
        """
        return AssisteActivite.query.filter_by(id_spectateur=id_spectateur,
                                                id_activite=self.id_activite).first() is not None

class Groupe(db.Model) :
    """Classe de groupe.

    Args:
        db (class): Classe de base de données.

    Returns:
        Groupe: Groupe.
    """
    __tablename__ = 'Groupe'
    id_groupe = db.Column(db.Integer, primary_key=True)
    nom_groupe = db.Column(db.String(50), nullable=False)
    id_genre_musical = db.Column(db.Integer,
                                db.ForeignKey('Genre_Musical.id_genre_musical'), nullable=False)
    date_arrivee = db.Column(db.Date, nullable=False)
    date_depart = db.Column(db.Date, nullable=False)
    heure_arrivee = db.Column(db.Time, nullable=False)
    heure_depart = db.Column(db.Time, nullable=False)

    genre_musical = db.relationship('GenreMusical', backref=db.backref('Genre_Musical', lazy=True))

    def __init__(self, nom, id_genre, date_arrivee, date_depart, heure_arrivee, heure_depart) :
        """Fonction de construction d'un groupe.

        Args:
            nom (str): Nom du groupe.
            id_genre_musical (int): Identifiant du genre musical du groupe.
            date_arrivee (date): Date d'arrivée du groupe.
            date_depart (date): Date de départ du groupe.
            heure_arrivee (time): Heure d'arrivée du groupe.
            heure_depart (time): Heure de départ du groupe.
        """
        self.nom_groupe = nom
        self.id_genre_musical = id_genre
        self.date_arrivee = date_arrivee
        self.date_depart = date_depart
        self.heure_arrivee = heure_arrivee
        self.heure_depart = heure_depart

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire du groupe.
        """
        return {
            'id': self.id_groupe,
            'nom': self.nom_groupe,
            'genre': self.genre_musical.to_dict() if self.genre_musical else None,
            'date_arrivee': self.date_arrivee,
            'date_depart': self.date_depart,
            'heure_arrivee': self.heure_arrivee,
            'heure_depart': self.heure_depart,
            'concerts': self.get_concerts_dict(),
            'nb_membres': len(self.get_membres()),
            'hebergement': self.get_hebergement().to_dict() if self.get_hebergement() else None,
            'activites': [participe.activite.to_dict() for participe in Participer.query.filter_by(
                id_groupe=self.id_groupe).all()],
        }

    def get_photo(self) :
        """Fonction de récupération de la photo du groupe.

        Returns:
            Photos: Photo du groupe.
        """
        return Photos.query.filter_by(id_group=self.id_groupe).first()

    def get_genre(self) :
        """Fonction de récupération du genre musical du groupe.

        Returns:
            GenreMusical: Genre musical du groupe.
        """
        return GenreMusical.query.filter_by(id_genre_musical=self.id_genre_musical).first()

    def get_membres(self) :
        """Fonction de récupération des membres du groupe.

        Returns:
            list: Liste des membres du groupe.
        """
        return Artiste.query.filter_by(id_groupe=self.id_groupe).all()

    def get_reseaux(self) :
        """Fonction de récupération des réseaux sociaux du groupe.

        Returns:
            list: Liste des réseaux sociaux du groupe.
        """
        return ReseauxSociaux.query.filter_by(id_group=self.id_groupe).all()

    def est_favoris(self, id_spectateur) :
        """Fonction de vérification de l'ajout du groupe aux favoris d'un spectateur.

        Args:
            id_spectateur (int): Identifiant du spectateur.

        Returns:
            bool: Vrai si le groupe est dans les favoris du spectateur, faux sinon.
        """
        return Favoris.query.filter_by(
            id_group=self.id_groupe, id_spectateur=id_spectateur).first() is not None

    def get_date_et_heure_arrive(self) :
        """Fonction de récupération de la date et de l'heure d'arrivée du groupe.

        Returns:
            datetime: Date et heure d'arrivée du groupe.
        """
        return datetime.combine(self.date_arrivee, self.heure_arrivee)

    def get_date_et_heure_depart(self) :
        """Fonction de récupération de la date et de l'heure de départ du groupe.

        Returns:
            datetime: Date et heure de départ du groupe.
        """
        return datetime.combine(self.date_depart, self.heure_depart)

    def get_concerts_dict(self) :
        """Fonction de récupération des concerts du groupe.

        Returns:
            list: Liste des concerts du groupe.
        """
        for se_produire in SeProduire.query.filter_by(id_groupe=self.id_groupe).all():
            concert = Concert.query.get(se_produire.id_concert)
            if concert:
                yield concert.to_dict()
        return []

    def get_logement(self) :
        """Fonction de récupération du logement du groupe.

        Returns:
            SeLoger: Logement du groupe.
        """
        return SeLoger.query.filter_by(id_groupe=self.id_groupe).first()

    def get_hebergement(self) :
        """Fonction de récupération de l'hébergement du groupe.

        Returns:
            Hebergement: Hébergement du groupe.
        """
        return Hebergement.query.get(
            self.get_logement().id_hebergement) if self.get_logement() else None

    def get_nb_membres(self) :
        """Fonction de récupération du nombre de membres du groupe.

        Returns:
            int: Nombre de membres du groupe.
        """
        return len(self.get_membres())

    def get_concerts(self) :
        """Fonction de récupération des concerts du groupe.

        Returns:
            list: Liste des concerts du groupe.
        """
        return SeProduire.query.filter_by(id_groupe=self.id_groupe).all()

    def get_nb_concerts(self) :
        """Fonction de récupération du nombre de concerts du groupe.

        Returns:
            int: Nombre de concerts du groupe.
        """
        return len(self.get_concerts())

    def get_activites(self) :
        """Fonction de récupération des activités du groupe.

        Returns:
            list: Liste des activités du groupe.
        """
        return Participer.query.filter_by(id_groupe=self.id_groupe).all()

class Artiste(db.Model) :
    """Classe d'artiste.

    Args:
        db (class): Classe de base de données.
    """
    __tablename__ = 'Artiste'
    id_artiste = db.Column(db.Integer, primary_key=True)
    nom_artiste = db.Column(db.String(50), nullable=False)
    prenom_artiste = db.Column(db.String(50), nullable=False)
    instrument_artiste = db.Column(db.String(50), nullable=False)
    id_groupe = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), nullable=False)

    groupe = db.relationship('Groupe', backref=db.backref('Groupe', lazy=True))

    def __init__(self, nom, prenom, instrument, id_groupe) :
        """Fonction de construction d'un artiste.

        Args:
            nom (str): Nom de l'artiste.
            prenom (str): Prénom de l'artiste.
            instrument (str): Instrument de l'artiste.
            id_groupe (int): Identifiant du groupe de l'artiste.
        """
        self.nom_artiste = nom
        self.prenom_artiste = prenom
        self.instrument_artiste = instrument
        self.id_groupe = id_groupe

    def get_groupe(self) :
        """Fonction de récupération du groupe de l'artiste.

        Returns:
            Groupe: Groupe de l'artiste.
        """
        return Groupe.query.get(self.id_groupe)

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire de l'artiste.
        """
        return {
            'id': self.id_artiste,
            'nom': self.nom_artiste,
            'prenom': self.prenom_artiste,
            'instrument': self.instrument_artiste,
            'groupe': self.groupe.to_dict() if self.groupe else None,
        }

class Concert(db.Model) :
    """Classe de concert.

    Args:
        db (class): Classe de base de données.

    Returns:
        Concert: Concert.
    """
    __tablename__ = 'Concert'
    id_concert = db.Column(db.Integer, primary_key=True, autoincrement = True)
    nom_concert = db.Column(db.String(50), nullable=False)
    date_concert = db.Column(db.Date, nullable=False)
    heure_debut_concert = db.Column(db.Time, nullable=False)
    duree_concert = db.Column(db.Time, nullable=False)
    temps_montage = db.Column(db.Time, nullable=False)
    temps_demontage = db.Column(db.Time, nullable=False)
    id_lieu = db.Column(db.Integer, db.ForeignKey('Lieu.id_lieu'), nullable=False)
    id_genre_musical = db.Column(db.Integer,
                                db.ForeignKey('Genre_Musical.id_genre_musical'), nullable=False)

    lieu = db.relationship('Lieu', backref=db.backref('Lieu', lazy=True))
    genre_musical = db.relationship('GenreMusical', backref=db.backref('genre', lazy=True))

    __table_args__ = (
        CheckConstraint('temps_montage + temps_demontage < duree_concert'),
        CheckConstraint('temps_montage > 0'),
        CheckConstraint('temps_demontage > 0'),
        CheckConstraint('duree_concert > 0'),
    )

    def __init__(self, nom, date,heure_debut, duree, montage, demontage, id_lieu, id_genre) :
        """Fonction de construction d'un concert.

        Args:
            nom (str): Nom du concert.
            date (date): Date du concert.
            heure_debut (time): Heure de début du concert.
            duree (time): Durée du concert.
            montage (time): Temps de montage du concert.
            demontage (time): Temps de démontage du concert.
            id_lieu (int): Identifiant du lieu du concert.
            id_genre (int): Identifiant du genre musical du concert.
        """
        self.nom_concert = nom
        self.date_concert = date
        self.heure_debut_concert = heure_debut
        self.duree_concert = duree
        self.temps_montage = montage
        self.temps_demontage = demontage
        self.id_lieu = id_lieu
        self.id_genre_musical = id_genre

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire du concert.
        """
        return {
            'id': self.id_concert,
            'nom': self.nom_concert,
            'date': self.date_concert,
            'heure_debut': self.heure_debut_concert,
            'duree': self.duree_concert,
            'montage': self.temps_montage,
            'demontage': self.temps_demontage,
            'lieu': self.lieu.to_dict() if self.lieu else None,
            'genre': self.genre_musical.to_dict() if self.genre_musical else None,
        }

    def get_date_fin(self) :
        """Fonction de récupération de la date de fin du concert.

        Returns:
            date: Date de fin du concert.
        """
        debut = self.heure_debut_concert
        duree = self.duree_concert
        diff_debut = timedelta(hours=debut.hour, minutes=debut.minute, seconds=debut.second)
        diff_duree = timedelta(hours=duree.hour, minutes=duree.minute, seconds=duree.second)
        difference = diff_debut + diff_duree
        return (datetime.min + difference).time()

class StyleMusical(db.Model) :
    """Classe de style musical.

    Args:
        db (class): Classe de base de données.
    """
    __tablename__ = 'Style_Musical'
    id_style_musical = db.Column(db.Integer, primary_key=True)
    nom_style_musical = db.Column(db.String(50), nullable=False)
    id_genre_musical = db.Column(db.Integer,
                                db.ForeignKey('Genre_Musical.id_genre_musical'), nullable=False)

    genre_musical = db.relationship('GenreMusical', backref=db.backref('style_genre', lazy=True))

    def __init__ (self, nom, id_genre_musical) :
        """Fonction de construction d'un style musical.

        Args:
            nom (str): Nom du style musical.
            id_genre_musical (int): Identifiant du genre musical du style musical.
        """
        self.nom_style_musical = nom
        self.id_genre_musical = id_genre_musical

    def get_genre(self) :
        """Fonction de récupération du genre musical du style musical.

        Returns:
            GenreMusical: Genre musical du style musical.
        """
        return GenreMusical.query.filter_by(id_genre_musical=self.id_genre_musical).first()

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire du style musical.
        """
        return {
            'id': self.id_style_musical,
            'nom': self.nom_style_musical,
            'genre': self.genre_musical.to_dict() if self.genre_musical else None,
        }

class Billet(db.Model) :
    """Classe de billet.

    Args:
        db (class): Classe de base de données.

    Returns:
        Billet: Billet.
    """
    __tablename__ = 'Billet'
    id_billet = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_spectateur = db.Column(db.Integer, db.ForeignKey('Spectateur.id_spectateur'), nullable=False)
    id_fest = db.Column(db.Integer, db.ForeignKey('Festival.id_fest'), nullable=False)
    id_type_billet = db.Column(db.String(50),
                            db.ForeignKey('Type_Billet.id_type_billet'), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)

    spectateur = db.relationship('Spectateur', backref='billets', lazy=True)
    festival = db.relationship('Festival', backref='billets', lazy=True)

    __table_args__ = (
        CheckConstraint('id_spectateur > 0'),
        CheckConstraint('id_fest > 0'),
    )

    def __init__(self, id_spectateur, id_festival, id_type_billet, date_debut) :
        """Fonction de construction d'un billet.

        Args:
            id_spectateur (int): Identifiant du spectateur.
            id_festival (int): Identifiant du festival.
            id_type_billet (int): Identifiant du type de billet.
            date_debut (date): Date de début du billet.
        """
        self.id_spectateur = id_spectateur
        self.id_fest = id_festival
        self.id_type_billet = id_type_billet
        self.date_debut = date_debut

    def get_spectateur(self) :
        """Fonction de récupération du spectateur.

        Returns:
            Spectateur: Spectateur.
        """
        return Spectateur.query.get(int(self.id_spectateur))

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire du billet.
        """
        diff= timedelta(days=TypeBillet.query.get(self.id_type_billet).duree_validite_type_billet-1)
        return {
            'id': self.id_billet,
            'id_spectateur': self.id_spectateur,
            'id_festival': self.id_fest,
            'id_type_billet': self.id_type_billet,
            'nom_type_billet': TypeBillet.query.get(self.id_type_billet).nom_type_billet,
            'festival': self.festival.to_dict() if self.festival else None,
            'spectateur': self.spectateur.to_dict() if self.spectateur else None,
            'date_debut': self.date_debut,
            'date_fin': (self.date_debut + diff) if self.date_debut else None,
        }

class TypeBillet(db.Model) :
    """Classe de type de billet.

    Args:
        db (class): Classe de base de données.

    Returns:
        TypeBillet: Type de billet.
    """
    __tablename__ = 'Type_Billet'
    id_type_billet = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_type_billet = db.Column(db.String(50))
    duree_validite_type_billet = db.Column(db.Integer, nullable=False)
    prix_type_billet = db.Column(db.Float, nullable=False)
    quantite_initiale_disponible_type_billet = db.Column(db.Integer, nullable=False)

    billets = db.relationship('Billet', backref='type_billet', lazy=True)

    def __init__(self, nom, duree_validite, prix, quantite_initiale_disponible) :
        """Fonction de construction d'un type de billet.

        Args:
            nom (str): Nom du type de billet.
            duree_validite (int): Durée de validité du type de billet.
            prix (float): Prix du type de billet.
            quantite_initiale_disponible (int): Quantité initiale disponible du type de billet.
        """
        self.nom_type_billet = nom
        self.duree_validite_type_billet = duree_validite
        self.prix_type_billet = prix
        self.quantite_initiale_disponible_type_billet = quantite_initiale_disponible

    def get_billets(self) :
        """Fonction de récupération des billets du type de billet.

        Returns:
            list: Liste des billets du type de billet.
        """
        return Billet.query.filter_by(id_type_billet=self.id_type_billet).all()

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire du type de billet.
        """
        return {
            'id': self.id_type_billet,
            'nom': self.nom_type_billet,
            'duree': self.duree_validite_type_billet,
            'prix': self.prix_type_billet,
            'quantite_dispo': self.quantite_initiale_disponible_type_billet,
            'quantite_reservee': len(self.billets) if self.billets else 0,
        }

class Organise(db.Model) :
    """Classe d'organisation.

    Args:
        db (class): Classe de base de données.
    """
    __tablename__ = 'Organise'
    id_activite = db.Column(db.Integer, db.ForeignKey('Activite.id_activite'), primary_key=True)
    id_lieu = db.Column(db.Integer, db.ForeignKey('Lieu.id_lieu'), primary_key=True)

    activite = db.relationship('Activite', backref=db.backref('Activite', lazy=True))
    lieu = db.relationship('Lieu', backref=db.backref('organise_lieu', lazy=True))

    def __init__(self, id_activite, id_lieu) :
        """Fonction de construction d'une organisation.

        Args:
            id_activite (int): Identifiant de l'activité.
            id_lieu (int): Identifiant du lieu.
        """
        self.id_activite = id_activite
        self.id_lieu = id_lieu

    def get_activite(self) :
        """Fonction de récupération de l'activité.

        Returns:
            Activite: Activité.
        """
        return Activite.query.get(int(self.id_activite))

    def get_lieu(self) :
        """Fonction de récupération du lieu.

        Returns:
            Lieu: Lieu.
        """
        return Lieu.query.get(int(self.id_lieu))

class Participer(db.Model) :
    """Classe de participation.

    Args:
        db (class): Classe de base de données.

    Returns:
        Participer: Participation.
    """
    __tablename__ = 'Participer'
    id_groupe = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), primary_key=True)
    id_activite = db.Column(db.Integer, db.ForeignKey('Activite.id_activite'), primary_key=True)

    groupe = db.relationship('Groupe', backref=db.backref('participer_groupe', lazy=True))
    activite = db.relationship('Activite', backref=db.backref('participer_activite', lazy=True))

    def __init__(self, id_groupe, id_activite) :
        """Fonction de construction d'une participation.

        Args:
            id_groupe (int): Identifiant du groupe.
            id_activite (int): Identifiant de l'activité.
        """
        self.id_groupe = id_groupe
        self.id_activite = id_activite

    def get_activite(self) :
        """Fonction de récupération de l'activité.

        Returns:
            Activite: Activité.
        """
        return Activite.query.get(int(self.id_activite))

    def get_groupe(self) :
        """Fonction de récupération du groupe.

        Returns:
            Groupe: Groupe.
        """
        return Groupe.query.get(int(self.id_groupe))

class SeLoger(db.Model) :
    """Classe de logement.

    Args:
        db (class): Classe de base de données.
    """
    __tablename__ = 'Se_Loger'
    id_se_loger = db.Column(db.Integer, primary_key=True, autoincrement = True)
    id_groupe = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'))
    id_hebergement = db.Column(db.Integer, db.ForeignKey('Hebergement.id_hebergement'))
    date_arrivee = db.Column(db.Date, nullable=False)
    date_depart = db.Column(db.Date, nullable=False)

    groupe = db.relationship('Groupe', backref=db.backref('se_loger_groupe', lazy=True))
    hebergement = db.relationship('Hebergement', backref=db.backref('Hebergement', lazy=True))

    def __init__(self, id_groupe, id_hebergement, date_arrivee, date_depart) :
        """Fonction de construction d'un logement.

        Args:
            id_groupe (int): Identifiant du groupe.
            id_hebergement (int): Identifiant de l'hébergement.
            date_arrivee (date): Date d'arrivée.
            date_depart (date): Date de départ.
        """
        self.id_groupe = id_groupe
        self.id_hebergement = id_hebergement
        self.date_arrivee = date_arrivee
        self.date_depart = date_depart

    def get_hebergement(self) :
        """Fonction de récupération de l'hébergement.

        Returns:
            Hebergement: Hébergement.
        """
        return Hebergement.query.get(int(self.id_hebergement))

    def get_groupe(self) :
        """Fonction de récupération du groupe.

        Returns:
            Groupe: Groupe.
        """
        return Groupe.query.get(int(self.id_groupe))

class SeProduire(db.Model) :
    """Classe de production.

    Args:
        db (class): Classe de base de données.

    Returns:
        SeProduire: Production.
    """
    __tablename__ = 'Se_Produire'
    id_groupe = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), primary_key=True)
    id_concert = db.Column(db.Integer, db.ForeignKey('Concert.id_concert'), primary_key=True)

    groupe = db.relationship('Groupe', backref=db.backref('se_produire_groupe', lazy=True))
    concert = db.relationship('Concert', backref=db.backref('Concert', lazy=True))

    def __init__(self, id_groupe, id_concert) :
        """Fonction de construction d'une production.

        Args:
            id_groupe (int): Identifiant du groupe.
            id_concert (int): Identifiant du concert.
        """
        self.id_groupe = id_groupe
        self.id_concert = id_concert

    def get_concert(self) :
        """Fonction de récupération du concert.

        Returns:
            Concert: Concert.
        """
        return Concert.query.get(int(self.id_concert))

    def get_groupe(self) :
        """Fonction de récupération du groupe.

        Returns:
            Groupe: Groupe.
        """
        return Groupe.query.get(int(self.id_groupe))

class FestivalLieu(db.Model) :
    """Classe de relation entre festival et lieu.

    Args:
        db (class): Classe de base de données.
    """
    id_fest = db.Column(db.Integer, db.ForeignKey('Festival.id_fest'), primary_key=True)
    id_lieu = db.Column(db.Integer, db.ForeignKey('Lieu.id_lieu'), primary_key=True)

    festival = db.relationship('Festival', backref=db.backref('Festival', lazy=True))
    lieu = db.relationship('Lieu', backref=db.backref('festival_lieu_relation', lazy=True))

    def __init__(self, id_fest, id_lieu) :
        """Fonction de construction d'une relation entre festival et lieu.

        Args:
            id_fest (int): Identifiant du festival.
            id_lieu (int): Identifiant du lieu.
        """
        self.id_fest = id_fest
        self.id_lieu = id_lieu

    def get_festival(self) :
        """Fonction de récupération du festival.

        Returns:
            Festival: Festival.
        """
        return Festival.query.get(int(self.id_fest))

    def get_lieu(self) :
        """Fonction de récupération du lieu.

        Returns:
            Lieu: Lieu.
        """
        return Lieu.query.get(int(self.id_lieu))

class ReseauxSociaux(db.Model) :
    """Classe de réseaux sociaux.

    Args:
        db (class): Classe de base de données.
    """
    __tablename__ = 'Reseaux_Sociaux'
    id_reseaux_sociaux = db.Column(db.Integer, primary_key=True)
    nom_reseaux_sociaux = db.Column(db.String(50), nullable=False)
    url_reseaux_sociaux = db.Column(db.String(50), nullable=False)
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), nullable=False)

    groupe = db.relationship('Groupe', backref=db.backref('reseau_groupe_relation', lazy=True))

    def __init__(self, nom, url, id_group) :
        """Fonction de construction d'un réseau social.

        Args:
            nom (str): Nom du réseau social.
            url (str): URL du réseau social.
            id_group (int): Identifiant du groupe.
        """
        self.nom_reseaux_sociaux = nom
        self.url_reseaux_sociaux = url
        self.id_group = id_group

    def get_group(self) :
        """Fonction de récupération du groupe.

        Returns:
            Groupe: Groupe.
        """
        return Groupe.query.get(int(self.id_group))

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire du réseau social.
        """
        return {
            'id': self.id_reseaux_sociaux,
            'nom': self.nom_reseaux_sociaux,
            'url': self.url_reseaux_sociaux,
            'id_group': self.id_group,
        }

class Photos(db.Model) :
    """Classe de photos.

    Args:
        db (class): Classe de base de données.

    Returns:
        Photos: Photo.
    """
    __tablename__ = 'Photos'
    id_photos = db.Column(db.Integer, primary_key=True)
    url_photos = db.Column(db.String(50), nullable=False)
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), nullable=False)

    groupe = db.relationship('Groupe', backref=db.backref('photos_groupe_relation', lazy=True))

    def __init__(self, url, id_group) :
        """Fonction de construction d'une photo.

        Args:
            url (str): URL de la photo.
            id_group (int): Identifiant du groupe.
        """
        self.url_photos = url
        self.id_group = id_group

    def get_group(self) :
        """Fonction de récupération du groupe.

        Returns:
            Groupe: Groupe.
        """
        return Groupe.query.get(int(self.id_group))

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire de la photo.
        """
        return {
            'id': self.id_photos,
            'url': self.url_photos,
            'id_group': self.id_group,
        }

class Videos(db.Model) :
    """Classe de vidéos.

    Args:
        db (class): Classe de base de données.

    Returns:
        Videos: Vidéo.
    """
    __tablename__ = 'Videos'
    id_videos = db.Column(db.Integer, primary_key=True)
    url_videos = db.Column(db.String(50), nullable=False)
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), nullable=False)

    groupe = db.relationship('Groupe', backref=db.backref('videos_groupe_relation', lazy=True))

    def __init__(self, url, id_group) :
        """Fonction de construction d'une vidéo.

        Args:
            url (str): URL de la vidéo.
            id_group (int): Identifiant du groupe.
        """
        self.url_videos = url
        self.id_group = id_group

    def get_group(self) :
        """Fonction de récupération du groupe.

        Returns:
            Groupe: Groupe.
        """
        return Groupe.query.get(int(self.id_group))

    def to_dict(self) :
        """Fonction de conversion en dictionnaire.

        Returns:
            dict: Dictionnaire de la vidéo.
        """
        return {
            'id': self.id_videos,
            'url': self.url_videos,
            'id_group': self.id_group,
        }

class Favoris(db.Model) :
    """Classe de favoris.

    Args:
        db (class): Classe de base de données.

    Returns:
        Favoris: Favoris.
    """
    __tablename__ = 'Favoris'
    id_favoris = db.Column(db.Integer, primary_key=True)
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), nullable=False)
    id_spectateur = db.Column(db.Integer, db.ForeignKey('Spectateur.id_spectateur'), nullable=False)

    groupe = db.relationship('Groupe', backref=db.backref('favoris_groupe_relation', lazy=True))
    spectateur = db.relationship('Spectateur',
                                backref=db.backref('favoris_spectateur_relation', lazy=True))

    def __init__(self, id_group, id_spectateur) :
        """Fonction de construction d'un favoris.

        Args:
            id_group (int): Identifiant du groupe.
            id_spectateur (int): Identifiant du spectateur.
        """
        self.id_group = id_group
        self.id_spectateur = id_spectateur

    def get_group(self) :
        """Fonction de récupération du groupe.

        Returns:
            Groupe: Groupe.
        """
        return Groupe.query.get(int(self.id_group))

    def get_spectateur(self) :
        """Fonction de récupération du spectateur.

        Returns:
            Spectateur: Spectateur.
        """
        return Spectateur.query.get(int(self.id_spectateur))

class Assiste(db.Model) :
    """Classe pour assister à un concert.

    Args:
        db (class): Classe de base de données.
    """
    __tablename__ = 'Assiste'
    id_spectateur = db.Column(db.Integer,
                            db.ForeignKey('Spectateur.id_spectateur'), primary_key=True)
    id_concert = db.Column(db.Integer, db.ForeignKey('Concert.id_concert'), primary_key=True)

    spectateur = db.relationship('Spectateur', backref=db.backref('Assiste', lazy=True))
    concert = db.relationship('Concert', backref=db.backref('Assiste', lazy=True))

    def __init__(self, id_spectateur, id_concert) :
        """Fonction de construction d'une relation entre spectateur et concert.

        Args:
            id_spectateur (int): Identifiant du spectateur.
            id_concert (int): Identifiant du concert.
        """
        self.id_spectateur = id_spectateur
        self.id_concert = id_concert

    def get_concert(self) :
        """Fonction de récupération du concert.

        Returns:
            Concert: Concert.
        """
        return Concert.query.get(int(self.id_concert))

    def get_spectateur(self) :
        """Fonction de récupération du spectateur.

        Returns:
            Spectateur: Spectateur.
        """
        return Spectateur.query.get(int(self.id_spectateur))

class AssisteActivite(db.Model) :
    """Classe pour assister à une activité.

    Args:
        db (class): Classe de base de données.
    """
    __tablename__ = 'AssisteActivite'
    id_spectateur = db.Column(db.Integer,
                            db.ForeignKey('Spectateur.id_spectateur'), primary_key=True)
    id_activite = db.Column(db.Integer, db.ForeignKey('Activite.id_activite'), primary_key=True)

    spectateur = db.relationship('Spectateur', backref=db.backref('AssisteActivite', lazy=True))
    activite = db.relationship('Activite', backref=db.backref('AssisteActivite', lazy=True))

    def __init__(self, id_spectateur, id_activite) :
        """Fonction de construction d'une relation entre spectateur et activité.

        Args:
            id_spectateur (int): Identifiant du spectateur.
            id_activite (int): Identifiant de l'activité.
        """
        self.id_spectateur = id_spectateur
        self.id_activite = id_activite

    def get_activite(self) :
        """Fonction de récupération de l'activité.

        Returns:
            Activite: Activité.
        """
        return Activite.query.get(int(self.id_activite))

    def get_spectateur(self) :
        """Fonction de récupération du spectateur.

        Returns:
            Spectateur: Spectateur.
        """
        return Spectateur.query.get(int(self.id_spectateur))

def ajouter_festival(id_fest, nom, date_debut, duree) :
    """Fonction d'ajout d'un festival.

    Args:
        id_fest (int): Identifiant du festival.
        nom (str): Nom du festival.
        date_debut (date): Date de début du festival.
        duree (int): Durée du festival.

    Returns:
        str: Message de confirmation de l'ajout du festival.
    """
    if not nom:
        return "Le nom du festival ne peut pas être vide"
    try:
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()

        festival = Festival(id_fest, nom, date_debut, duree)
        db.session.add(festival)
        db.session.commit()
        return f"Le festival {nom} a bien été ajouté"
    except ValueError as e:
        db.session.rollback()
        return "Erreur lors de la conversion de la date : " + str(e)
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def ajouter_lieu(nom, adresse, ville, code_postal, pays, capacite, type_lieu) :
    """Fonction d'ajout d'un lieu.

    Args:
        nom (str): Nom du lieu.
        adresse (str): Adresse du lieu.
        ville (str): Ville du lieu.
        code_postal (str): Code postal du lieu.
        pays (str): Pays du lieu.
        capacite (int): Capacité du lieu.
        type_lieu (str): Type du lieu.

    Returns:
        str: Message de confirmation de l'ajout du lieu.
    """
    if not nom:
        return "Le nom du lieu ne peut pas être vide"
    if not adresse:
        return "L'adresse du lieu ne peut pas être vide"
    if not ville:
        return "La ville du lieu ne peut pas être vide"
    if not code_postal:
        return "Le code postal du lieu ne peut pas être vide"
    if not pays:
        return "Le pays du lieu ne peut pas être vide"
    if not capacite:
        return "La capacité du lieu ne peut pas être vide"
    if not type_lieu:
        return "Le type du lieu ne peut pas être vide"
    try :
        lieu = Lieu(nom, adresse, ville, code_postal, pays, capacite, type_lieu)
        db.session.add(lieu)
        db.session.commit()
        return f"Le lieu {nom} a bien été ajouté"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    except ValueError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def ajouter_festival_lieu(id_fest, id_lieu) :
    """Fonction d'ajout d'un festival à un lieu.

    Args:
        id_fest (int): Identifiant du festival.
        id_lieu (int): Identifiant du lieu.

    Returns:
        str: Message de confirmation de l'ajout du festival au lieu.
    """
    try :
        festival_lieu = FestivalLieu(id_fest, id_lieu)
        db.session.add(festival_lieu)
        db.session.commit()
        return f"Le festival {id_fest} a bien été ajouté au lieu {id_lieu}"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    except ValueError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def get_types_billets() :
    """Fonction de récupération des types de billets.

    Returns:
        list: Liste des types de billets.
    """
    types_billets = []
    for type_billet in TypeBillet.query.all():
        types_billets.append(type_billet.to_dict())
    return types_billets

def ajouter_type_billet(nom, duree_validite, prix, quantite_initiale_disponible) :
    """Fonction d'ajout d'un type de billet.

    Args:
        nom (str): Nom du type de billet.
        duree_validite (int): Durée de validité du type de billet.
        prix (float): Prix du type de billet.
        quantite_initiale_disponible (int): Quantité initiale disponible du type de billet.

    Returns:
        str: Message de confirmation de l'ajout du type de billet.
    """
    if not nom:
        return "Le nom du type de billet ne peut pas être vide"
    if not duree_validite:
        return "La durée de validité du type de billet ne peut pas être vide"
    if not prix:
        return "Le prix du type de billet ne peut pas être vide"
    if not quantite_initiale_disponible:
        return "La quantité initiale disponible du type de billet ne peut pas être vide"
    try :
        type_billet = TypeBillet(nom, duree_validite, prix, quantite_initiale_disponible)
        db.session.add(type_billet)
        db.session.commit()
        return f"Le type de billet {nom} a bien été ajouté"
    except ValueError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def ajouter_genre_musical(nom_genre_musical) :
    """Fonction d'ajout d'un genre musical.

    Args:
        nom_genre_musical (str): Nom du genre musical.

    Returns:
        str: Message de confirmation de l'ajout du genre musical.
    """
    if not nom_genre_musical:
        return "Le nom du genre musical ne peut pas être vide"
    try :
        genre_musical = GenreMusical(nom_genre_musical)
        db.session.add(genre_musical)
        db.session.commit()
        return f"Le genre musical {nom_genre_musical} a bien été ajouté"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def get_jours_festival() :
    """Fonction de récupération des jours du festival.

    Returns:
        list: Liste des jours du festival.
    """
    jours_festival = []
    debut = Festival.query.first().date_debut_fest
    duree = Festival.query.first().duree_fest
    for i in range(duree):
        jours_festival.append(debut + timedelta(days=i))
    return jours_festival

def get_duree_fest() :
    """Fonction de récupération de la durée du festival.

    Returns:
        int: Durée du festival.
    """
    return Festival.query.first().duree_fest

def get_spectateur(nom, prebom) :
    """Fonction de récupération d'un spectateur.

    Args:
        nom (str): Nom du spectateur.
        prebom (str): Prénom du spectateur.

    Returns:
        Spectateur: Spectateur
    """
    return Spectateur.query.filter_by(nom_spectateur=nom, prenom_spectateur=prebom).first()

def get_spect_by_id(id_spect) :
    """Fonction de récupération d'un spectateur.

    Args:
        id_spec (int): Identifiant du spectateur.

    Returns:
        Spectateur: Spectateur.
    """
    return Spectateur.query.filter_by(id_spectateur = id_spect).first()

def add_billet(id_spect, id_festival, id_type_billet, date_debut) :
    """Fonction d'ajout d'un billet.

    Args:
        id_spec (int): Identifiant du spectateur.
        id_festival (int): Identifiant du festival.
        id_type_billet (int): Identifiant du type de billet.
        date_debut (date): Date de début du billet.

    Returns:
        str: Message de confirmation de l'ajout du billet.
    """
    try :
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()
        billet_existant = get_billet(id_spect, id_festival, id_type_billet, date_debut)
        if billet_existant:
            return False
        billet = Billet(id_spect, id_festival, id_type_billet, date_debut)
        db.session.add(billet)
        db.session.commit()
        return True
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def get_billet(id_spect, id_festival, id_type_billet, date_debut) :
    """Fonction de récupération d'un billet.

    Args:
        id_spect (int): Identifiant du spectateur.
        id_festival (int): Identifiant du festival.
        id_type_billet (int): Identifiant du type de billet.
        date_debut (date): Date de début du billet.

    Returns:
        Billet: Billet.
    """
    return Billet.query.filter_by(id_spectateur=id_spect,
                                id_fest=id_festival,
                                id_type_billet=id_type_billet, date_debut=date_debut).first()

def get_activites() :
    """Fonction de récupération des activités.

    Returns:
        list: Liste des activités.
    """
    activites = []
    for activite in Activite.query.all():
        activites.append(activite)
    return activites

def ajouter_groupe(nom_groupe, id_genre, date_arrivee, date_depart, heure_arrive, heure_depart) :
    """Fonction d'ajout d'un groupe.

    Args:
        nom_groupe (str): Nom du groupe.
        id_genre_musical (int): identifiant du genre musical.
        date_arrivee (date): Date d'arrivée du groupe.
        date_depart (date): Date de départ du groupe.
        heure_arrivee (time): Heure d'arrivée du groupe.
        heure_depart (time): Heure de départ du groupe.

    Returns:
        str: Message de confirmation de l'ajout du groupe.
    """
    if not nom_groupe:
        return "Le nom du groupe ne peut pas être vide"
    if not id_genre:
        return "L'id du genre musical ne peut pas être vide"
    if not date_arrivee:
        return "La date d'arrivée du groupe ne peut pas être vide"
    if not date_depart:
        return "La date de départ du groupe ne peut pas être vide"
    if not heure_arrive:
        return "L'heure d'arrivée du groupe ne peut pas être vide"
    if not heure_depart:
        return "L'heure de départ du groupe ne peut pas être vide"
    try :
        date_arrivee = datetime.strptime(date_arrivee, '%Y-%m-%d').date()
        date_depart = datetime.strptime(date_depart, '%Y-%m-%d').date()
        heure_arrive = datetime.strptime(heure_arrive, '%H:%M').time()
        heure_depart = datetime.strptime(heure_depart, '%H:%M').time()
        groupe = Groupe(nom_groupe, id_genre, date_arrivee, date_depart, heure_arrive, heure_depart)
        db.session.add(groupe)
        db.session.commit()
        return f"Le groupe {nom_groupe} a bien été ajouté"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    except ValueError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def ajouter_favoris(id_group, id_spectateur) :
    """Fonction d'ajout d'un favoris.

    Args:
        id_group (int): Identifiant du groupe.
        id_spectateur (int): Identifiant du spectateur.

    Returns:
        str: Message de confirmation de l'ajout du favoris.
    """
    if not id_group:
        return "L'id du groupe ne peut pas être vide"
    if not id_spectateur:
        return "L'id du spectateur ne peut pas être vide"
    try :
        favoris = Favoris(id_group, id_spectateur)
        db.session.add(favoris)
        db.session.commit()
        return f"Le groupe {id_group} a bien été ajouté aux favoris du spectateur {id_spectateur}"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    except ValueError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def ajouter_spectateur(nom_spectateur, prenom_spectateur, mot_de_passe_spectateur) :
    """Fonction d'ajout d'un spectateur.

    Args:
        nom_spectateur (str): Nom du spectateur.
        prenom_spectateur (str): Prénom du spectateur.
        mot_de_passe_spectateur (str): Mot de passe du spectateur.

    Returns:
        str: Message de confirmation de l'ajout du spectateur.
    """
    if not nom_spectateur:
        return "Le nom du spectateur ne peut pas être vide"
    if not prenom_spectateur:
        return "Le prénom du spectateur ne peut pas être vide"
    if not mot_de_passe_spectateur:
        return "Le mot de passe du spectateur ne peut pas être vide"
    try :
        m = sha256()
        m.update(mot_de_passe_spectateur.encode('utf-8'))
        spectateur = Spectateur(nom_spectateur, prenom_spectateur, m.hexdigest())
        db.session.add(spectateur)
        db.session.commit()
        return f"Le spectateur {nom_spectateur} {prenom_spectateur} a bien été ajouté"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    except ValueError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def ajouter_photos(url_photos, id_group) :
    """Fonction d'ajout d'une photo.

    Args:
        url_photos (str): URL de la photo.
        id_group (int): Identifiant du groupe.

    Returns:
        str: Message de confirmation de l'ajout de la photo.
    """
    if not url_photos:
        return "L'url de la photo ne peut pas être vide"
    if not id_group:
        return "L'id du groupe ne peut pas être vide"
    try :
        photos = Photos(url_photos, id_group)
        db.session.add(photos)
        db.session.commit()
        return f"La photo {url_photos} a bien été ajoutée au groupe {id_group}"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    except ValueError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def ajouter_artiste(nom_artiste, prenom_artiste, instrument_artiste, id_groupe) :
    """Fonction d'ajout d'un artiste.

    Args:
        nom_artiste (str): Nom de l'artiste.
        prenom_artiste (str): Prénom de l'artiste.
        instrument_artiste (str): Instrument de l'artiste.
        id_groupe (int): Identifiant du groupe.

    Returns:
        str: Message de confirmation de l'ajout de l'artiste.
    """
    if not nom_artiste:
        return "Le nom de l'artiste ne peut pas être vide"
    if not prenom_artiste:
        return "Le prénom de l'artiste ne peut pas être vide"
    if not instrument_artiste:
        return "L'instrument de l'artiste ne peut pas être vide"
    if not id_groupe:
        return "L'id du groupe ne peut pas être vide"
    try :
        artiste = Artiste(nom_artiste, prenom_artiste, instrument_artiste, id_groupe)
        db.session.add(artiste)
        db.session.commit()
        return f"L'artiste {nom_artiste} {prenom_artiste} a bien été ajouté"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    except ValueError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def ajouter_reseaux_sociaux(nom_reseaux_sociaux, url_reseaux_sociaux, id_group) :
    """Fonction d'ajout d'un réseau social.

    Args:
        nom_reseaux_sociaux (str): Nom du réseau social.
        url_reseaux_sociaux (str): URL du réseau social.
        id_group (int): Identifiant du groupe.

    Returns:
        str: Message de confirmation de l'ajout du réseau social.
    """
    if not nom_reseaux_sociaux:
        return "Le nom du réseau social ne peut pas être vide"
    if not url_reseaux_sociaux:
        return "L'url du réseau social ne peut pas être vide"
    if not id_group:
        return "L'id du groupe ne peut pas être vide"
    try :
        reseaux_sociaux = ReseauxSociaux(nom_reseaux_sociaux, url_reseaux_sociaux, id_group)
        db.session.add(reseaux_sociaux)
        db.session.commit()
        return f"Le réseau social {nom_reseaux_sociaux} a bien été ajouté au groupe {id_group}"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    except ValueError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def get_favoris_by_spec(id_spectateur) :
    """Fonction de récupération des favoris d'un spectateur.

    Args:
        id_spectateur (int): Identifiant du spectateur.

    Returns:
        list: Liste des favoris du spectateur.
    """
    return Favoris.query.filter_by(id_spectateur=id_spectateur).all()

def get_random_groupes() :
    """Fonction de récupération de 10 groupes aléatoires.

    Returns:
        list: Liste de 10 groupes aléatoires.
    """
    return Groupe.query.order_by(db.func.random()).limit(10).distinct().all()

def ajouter_se_produire(id_groupe, id_concert) :
    """Fonction d'ajout d'une production.

    Args:
        id_groupe (int): Identifiant du groupe.
        id_concert (int): Identifiant du concert.

    Returns:
        str: Message de confirmation de l'ajout de la production.
    """
    if not id_groupe:
        return "L'id du groupe ne peut pas être vide"
    if not id_concert:
        return "L'id du concert ne peut pas être vide"
    try :
        se_produire = SeProduire(id_groupe, id_concert)
        db.session.add(se_produire)
        db.session.commit()
        return f"Le groupe {id_groupe} a bien été ajouté au concert {id_concert}"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    except ValueError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def ajouter_concert(nom, date, debut_concert, duree, montage, demontage, id_lieu, id_genre) :
    """Fonction d'ajout d'un concert.

    Args:
        nom (str): Nom du concert.
        date (date): Date du concert.
        debut_concert (time): Heure de début du concert.
        duree (time): Durée du concert.
        montage (time): Temps de montage du concert.
        demontage (time): Temps de démontage du concert.
        id_lieu (int): Identifiant du lieu.
        id_genre (int): Identifiant du genre musical.

    Returns:
        str: Message de confirmation de l'ajout du concert.
    """
    if not nom:
        return "Le nom du concert ne peut pas être vide"
    if not date:
        return "La date du concert ne peut pas être vide"
    if not debut_concert:
        return "L'heure du concert ne peut pas être vide"
    if not duree:
        return "La durée du concert ne peut pas être vide"
    if not montage:
        return "Le temps de montage du concert ne peut pas être vide"
    if not demontage:
        return "Le temps de démontage du concert ne peut pas être vide"
    if not id_lieu:
        return "L'id du lieu ne peut pas être vide"
    if not id_genre:
        return "L'id du genre musical ne peut pas être vide"
    try :
        date = datetime.strptime(date, '%Y-%m-%d').date()
        debut_concert = datetime.strptime(debut_concert, '%H:%M').time()
        duree = datetime.strptime(duree, '%H:%M').time()
        montage = datetime.strptime(montage, '%H:%M').time()
        demontage = datetime.strptime(demontage, '%H:%M').time()
        concert = Concert(nom, date, debut_concert, duree, montage, demontage, id_lieu, id_genre)
        db.session.add(concert)
        db.session.commit()
        return f"Le concert {nom} a bien été ajouté"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    except ValueError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def assiste(id_spect, id_concert) :
    """Fonction d'ajout d'un spectateur à un concert.

    Args:
        id_spect (int): Identifiant du spectateur.
        id_concert (int): Identifiant du concert.

    Returns:
        str: Message de confirmation de l'ajout du spectateur au concert.
    """
    try :
        assister = Assiste(id_spect, id_concert)
        db.session.add(assister)
        db.session.commit()
        return f"Le spectateur {id_spect} assistera au concert {id_concert}"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def get_group(id_group) :
    """Fonction de récupération d'un groupe.

    Args:
        id_group (int): Identifiant du groupe.

    Returns:
        Groupe: Groupe.
    """
    return Groupe.query.filter_by(id_groupe=id_group).first()

def get_groupes() :
    """Fonction de récupération des groupes.

    Returns:
        list: Liste des groupes.
    """
    return Groupe.query.all()

def get_hebergement() :
    """Fonction de récupération des hébergements.

    Returns:
        list: Liste des hébergements.
    """
    return Hebergement.query.all()

def loger(id_group, id_hebergement) :
    """Fonction d'ajout d'un groupe à un hébergement.

    Args:
        id_group (int): Identifiant du groupe.
        id_hebergement (int): Identifiant de l'hébergement.

    Returns:
        str: Message de confirmation de l'ajout du groupe à l'hébergement.
    """
    try :
        group = Groupe.query.filter_by(id_groupe=id_group).first()
        if not group:
            return "Le groupe n'existe pas"
        if id_group is None:
            return "L'id du groupe ne peut pas être vide"
        groupe = group.to_dict()
        date_arrivee = groupe["date_arrivee"]
        date_depart = groupe["date_depart"]
        se_loger = SeLoger(id_groupe = id_group,
                        id_hebergement = id_hebergement,
                        date_arrivee = date_arrivee ,date_depart = date_depart)
        db.session.add(se_loger)
        db.session.commit()
        hebergement = Hebergement.query.filter_by(id_hebergement=id_hebergement).first()
        hebergement.capacite_hebergement -= groupe["nb_membres"]
        return f"Le groupe {id_group} sera logé à l'hébergement {id_hebergement}"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def ajouter_hebergement(nom, adresse, ville, code_postal, capacite_hebergement) :
    """Fonction d'ajout d'un hébergement.

    Args:
        nom (str): Nom de l'hébergement.
        adresse (str): Adresse de l'hébergement.
        ville (str): Ville de l'hébergement.
        code_postal (str): Code postal de l'hébergement.
        capacite_hebergement (int): Capacité de l'hébergement.

    Returns:
        str: Message de confirmation de l'ajout de l'hébergement.
    """
    if not nom:
        return "Le nom de l'hébergement ne peut pas être vide"
    if not adresse:
        return "L'adresse de l'hébergement ne peut pas être vide"
    if not ville:
        return "La ville de l'hébergement ne peut pas être vide"
    if not code_postal:
        return "Le code postal de l'hébergement ne peut pas être vide"
    if not capacite_hebergement:
        return "La capacité de l'hébergement ne peut pas être vide"
    try :
        hebergement = Hebergement(nom, adresse, ville, code_postal, capacite_hebergement)
        db.session.add(hebergement)
        db.session.commit()
        return f"L'hébergement {nom} a bien été ajouté"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def ajouter_activite(nom_activite, statut, date_activite, heure_debut_activite, duree_activite) :
    """Fonction d'ajout d'une activité.

    Args:
        nom_activite (str): Nom de l'activité.
        statut (str): Statut de l'activité.
        date_activite (date): Date de l'activité.
        heure_debut_activite (time): Heure de début de l'activité.
        duree_activite (time): Durée de l'activité.

    Returns:
        str: Message de confirmation de l'ajout de l'activité.
    """
    if not nom_activite:
        return "Le nom de l'activité ne peut pas être vide"
    if not date_activite:
        return "La date de l'activité ne peut pas être vide"
    if not heure_debut_activite:
        return "L'heure de l'activité ne peut pas être vide"
    if not duree_activite:
        return "La durée de l'activité ne peut pas être vide"
    if not statut:
        return "Le statut de l'activité ne peut pas être vide"
    try :
        statut = bool(statut == "Ouvert")
        date = datetime.strptime(date_activite, '%Y-%m-%d').date()
        heure = datetime.strptime(heure_debut_activite, '%H:%M').time()
        duree = datetime.strptime(duree_activite, '%H:%M').time()
        activite = Activite(nom_activite,statut, date, heure, duree)
        db.session.add(activite)
        db.session.commit()
        return f"L'activité {nom_activite} a bien été ajoutée"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def participe(id_groupe, id_activite) :
    """Fonction d'ajout d'un groupe à une activité.

    Args:
        id_groupe (int): Identifiant du groupe.
        id_activite (int): Identifiant de l'activité.

    Returns:
        str: Message de confirmation de l'ajout du groupe à l'activité.
    """
    try :
        participation = Participer(id_groupe, id_activite)
        db.session.add(participation)
        db.session.commit()
        return f"Le groupe {id_groupe} participe à l'activité {id_activite}"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def get_hebergement_by_id(id_hebergement) :
    """Fonction de récupération d'un hébergement.

    Args:
        id_hebergement (int): Identifiant de l'hébergement.

    Returns:
        Hebergement: Hébergement.
    """
    return Hebergement.query.filter_by(id_hebergement=id_hebergement).first()

def get_activite_by_id(id_activite) :
    """Fonction de récupération d'une activité.

    Args:
        id_activite (int): Identifiant de l'activité.

    Returns:
        Activite: Activité.
    """
    return Organise.query.filter_by(id_activite=id_activite).first()

def ajouter_organise(id_activite, id_lieu) :
    """Fonction d'ajout d'une activité à un lieu.

    Args:
        id_activite (int): Identifiant de l'activité.
        id_lieu (int): Identifiant du lieu.

    Returns:
        str: Message de confirmation de l'ajout de l'activité au lieu.
    """
    try :
        organise = Organise(id_activite, id_lieu)
        db.session.add(organise)
        db.session.commit()
        return f"L'activité {id_activite} est organisée au lieu {id_lieu}"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def inscrire(id_spectateur, id_activite) :
    """Fonction d'inscription d'un spectateur à une activité.

    Args:
        id_spectateur (int): Identifiant du spectateur.
        id_activite (int): Identifiant de l'activité.

    Returns:
        str: Message de confirmation de l'inscription du spectateur à l'activité.
    """
    try :
        inscrit = AssisteActivite(id_spectateur, id_activite)
        db.session.add(inscrit)
        db.session.commit()
        return f"Le spectateur {id_spectateur} est inscrit à l'activité {id_activite}"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def desinscrire(id_spectateur, id_activite) :
    """Fonction de désinscription d'un spectateur à une activité.

    Args:
        id_spectateur (int): Identifiant du spectateur.
        id_activite (int): Identifiant de l'activité.

    Returns:
        str: Message de confirmation de la désinscription du spectateur à l'activité.
    """
    try :
        AssisteActivite.query.filter_by(id_spectateur = id_spectateur,
                                        id_activite = id_activite).delete()
        db.session.commit()
        return f"Le spectateur {id_spectateur} est désinscrit à l'activité {id_activite}"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def get_favori(id_spectateur, id_groupe) :
    """Fonction de récupération d'un favori.

    Args:
        id_spectateur (int): Identifiant du spectateur.
        id_groupe (int): Identifiant du groupe.

    Returns:
        Favoris: Favoris.
    """
    return Favoris.query.filter_by(id_group=id_groupe, id_spectateur=id_spectateur).first()

@login_manager.user_loader
def load_user(id_spectateur) :
    """Fonction de chargement d'un utilisateur.

    Args:
        id_spectateur (int): Identifiant du spectateur.

    Returns:
        Spectateur: Spectateur.
    """
    return Spectateur.query.get(int(id_spectateur))
