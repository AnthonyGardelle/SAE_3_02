from .app import db, login_manager
from sqlalchemy import CheckConstraint
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class GenreMusical(db.Model):
    __tablename__ = 'Genre_Musical'
    id_genre_musical = db.Column(db.Integer, primary_key=True)
    nom_genre_musical = db.Column(db.String(50), nullable=False)
    
    def __init__(self, nom):
        self.nom_genre_musical = nom
    
class Lieu(db.Model):
    __tablename__ = 'Lieu'
    id_lieu = db.Column(db.Integer, primary_key=True)
    nom_lieu = db.Column(db.String(50), nullable=False)
    adresse_lieu = db.Column(db.String(50), nullable=False)
    ville_lieu = db.Column(db.String(50), nullable=False)
    code_postal_lieu = db.Column(db.String(50), nullable=False)
    pays_lieu = db.Column(db.String(50), nullable=False)
    capacite_lieu = db.Column(db.Integer, nullable=False)
    type_lieu = db.Column(db.String(50), nullable=False)
    
    def __init__(self, nom, adresse, ville, code_postal, pays, capacite, type_lieu):
        self.nom_lieu = nom
        self.adresse_lieu = adresse
        self.ville_lieu = ville
        self.code_postal_lieu = code_postal
        self.pays_lieu = pays
        self.capacite_lieu = capacite
        self.type_lieu = type_lieu

class Festival(db.Model):
    __tablename__ = 'Festival'
    id_fest = db.Column(db.Integer, primary_key=True)
    nom_fest = db.Column(db.String(50), nullable=False)
    date_debut_fest = db.Column(db.Date, nullable=False)
    duree_fest = db.Column(db.Integer, nullable=False)
    
    billets = db.relationship('Billet', backref='festival', lazy=True)
    
    def __init__(self, id_fest, nom, date_debut, duree):
        self.id_fest = id_fest
        self.nom_fest = nom
        self.date_debut_fest = date_debut
        self.duree_fest = duree
        
class Spectateur(db.Model):
    __tablename__ = 'Spectateur'
    id_spectateur = db.Column(db.Integer, primary_key=True)
    nom_spectateur = db.Column(db.String(50), nullable=False)
    prenom_spectateur = db.Column(db.String(50), nullable=False)
    
    def __init__(self, nom, prenom):
        self.nom_spectateur = nom
        self.prenom_spectateur = prenom
        
class Hebergement(db.Model):
    __tablename__ = 'Hebergement'
    id_hebergement = db.Column(db.Integer, primary_key=True)
    nom_hebergement = db.Column(db.String(50), nullable=False)
    adresse_hebergement = db.Column(db.String(50), nullable=False)
    ville_hebergement = db.Column(db.String(50), nullable=False)
    code_postal_hebergement = db.Column(db.String(50), nullable=False)
    capacite_hebergement = db.Column(db.Integer, nullable=False)
    
    def __init__(self, nom, adresse, ville, code_postal, capacite):
        self.nom_hebergement = nom
        self.adresse_hebergement = adresse
        self.ville_hebergement = ville
        self.code_postal_hebergement = code_postal
        self.capacite_hebergement = capacite

class Activite(db.Model):
    __tablename__ = 'Activite'
    id_activite = db.Column(db.Integer, primary_key=True)
    nom_activite = db.Column(db.String(50), nullable=False)
    statut = db.Column(db.String(50), nullable=False)
    date_debut_activite = db.Column(db.Date, nullable=False)
    duree_activite = db.Column(db.Integer, nullable=False)
    
    def __init__(self, nom, statut, date_debut, duree):
        self.nom_activite = nom
        self.statut = statut
        self.date_debut_activite = date_debut
        self.duree_activite = duree
        
class Groupe(db.Model):
    __tablename__ = 'Groupe'
    id_groupe = db.Column(db.Integer, primary_key=True)
    nom_groupe = db.Column(db.String(50), nullable=False)
    id_genre_musical = db.Column(db.Integer, db.ForeignKey('Genre_Musical.id_genre_musical'), nullable=False)
    
    genre_musical = db.relationship('GenreMusical', backref=db.backref('Genre_Musical', lazy=True))
    
    def __init__(self, nom, id_genre_musical):
        self.nom_groupe = nom
        self.id_genre_musical = id_genre_musical
        
class Artiste(db.Model):
    __tablename__ = 'Artiste'
    id_artiste = db.Column(db.Integer, primary_key=True)
    nom_artiste = db.Column(db.String(50), nullable=False)
    prenom_artiste = db.Column(db.String(50), nullable=False)
    instrument_artiste = db.Column(db.String(50), nullable=False)
    id_groupe = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), nullable=False)
    
    groupe = db.relationship('Groupe', backref=db.backref('Groupe', lazy=True))
    
    def __init__(self, nom, prenom, instrument, id_groupe):
        self.nom_artiste = nom
        self.prenom_artiste = prenom
        self.instrument_artiste = instrument
        self.id_groupe = id_groupe
        
class Concert(db.Model):
    __tablename__ = 'Concert'
    id_concert = db.Column(db.Integer, primary_key=True)
    nom_concert = db.Column(db.String(50), nullable=False)
    date_debut_concert = db.Column(db.Date, nullable=False)
    duree_concert = db.Column(db.Integer, nullable=False)
    temps_montage = db.Column(db.Integer, nullable=False)
    temps_demontage = db.Column(db.Integer, nullable=False)
    id_lieu = db.Column(db.Integer, db.ForeignKey('Lieu.id_lieu'), nullable=False)
    id_genre_musical = db.Column(db.Integer, db.ForeignKey('Genre_Musical.id_genre_musical'), nullable=False)

    lieu = db.relationship('Lieu', backref=db.backref('Lieu', lazy=True))
    genre_musical = db.relationship('GenreMusical', backref=db.backref('genre', lazy=True))

    __table_args__ = (
        CheckConstraint('temps_montage + temps_demontage < duree_concert'),
        CheckConstraint('temps_montage > 0'),
        CheckConstraint('temps_demontage > 0'),
        CheckConstraint('duree_concert > 0'),
    )

    def __init__(self, nom, date_debut, duree, montage, demontage, id_lieu, id_genre_musical):
        self.nom_concert = nom
        self.date_debut_concert = date_debut
        self.duree_concert = duree
        self.temps_montage = montage
        self.temps_demontage = demontage
        self.id_lieu = id_lieu
        self.id_genre_musical = id_genre_musical


class StyleMusical(db.Model):
    __tablename__ = 'Style_Musical'
    id_style_musical = db.Column(db.Integer, primary_key=True)
    nom_style_musical = db.Column(db.String(50), nullable=False)
    id_genre_musical = db.Column(db.Integer, db.ForeignKey('Genre_Musical.id_genre_musical'), nullable=False)
    
    genre_musical = db.relationship('GenreMusical', backref=db.backref('style_genre', lazy=True))
    
    def __init__ (self, nom, id_genre_musical):
        self.nom_style_musical = nom
        self.id_genre_musical = id_genre_musical
        
class Billet(db.Model):
    __tablename__ = 'Billet'
    id_billet = db.Column(db.Integer, primary_key=True)
    prix_billet = db.Column(db.Float, nullable=False)
    duree_validite_billet = db.Column(db.Integer, nullable=False)
    quantite_disponible = db.Column(db.Integer, nullable=False)
    id_spectateur = db.Column(db.Integer, db.ForeignKey('Spectateur.id_spectateur'), nullable=False)
    id_fest = db.Column(db.Integer, db.ForeignKey('Festival.id_fest'), nullable=False)

    spectateur = db.relationship('Spectateur', backref=db.backref('Spectateur', lazy=True))

    __table_args__ = (
        CheckConstraint('prix_billet > 0'),
        CheckConstraint('duree_validite_billet > 0'),
        CheckConstraint('quantite_disponible > 0'),
    )

    def __init__(self, prix, duree_validite, quantite, id_spectateur, id_festival):
        self.prix_billet = prix
        self.duree_validite_billet = duree_validite
        self.quantite_disponible = quantite
        self.id_spectateur = id_spectateur
        self.id_fest = id_festival
    
class Organise(db.Model):
    __tablename__ = 'Organise'
    id_activite = db.Column(db.Integer, db.ForeignKey('Activite.id_activite'), primary_key=True)
    id_lieu = db.Column(db.Integer, db.ForeignKey('Lieu.id_lieu'), primary_key=True)
    
    activite = db.relationship('Activite', backref=db.backref('Activite', lazy=True))
    lieu = db.relationship('Lieu', backref=db.backref('organise_lieu', lazy=True))
    
    def __init__(self, id_activite, id_lieu):
        self.id_activite = id_activite
        self.id_lieu = id_lieu

class Participer(db.Model):
    __tablename__ = 'Participer'
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), primary_key=True)
    id_activite = db.Column(db.Integer, db.ForeignKey('Activite.id_activite'), primary_key=True)
    
    groupe = db.relationship('Groupe', backref=db.backref('participer_groupe', lazy=True))
    activite = db.relationship('Activite', backref=db.backref('participer_activite', lazy=True))
    
    def __init__(self, id_groupe, id_activite):
        self.id_groupe = id_groupe
        self.id_activite = id_activite
        
class SeLoger(db.Model):
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), primary_key=True)
    id_hebergement = db.Column(db.Integer, db.ForeignKey('Hebergement.id_hebergement'), primary_key=True)
    date_arrivee = db.Column(db.Date, nullable=False)
    date_depart = db.Column(db.Date, nullable=False)
    
    groupe = db.relationship('Groupe', backref=db.backref('se_loger_groupe', lazy=True))
    hebergement = db.relationship('Hebergement', backref=db.backref('Hebergement', lazy=True))
    
    def __init__(self, id_groupe, id_hebergement, date_arrivee, date_depart):
        self.id_groupe = id_groupe
        self.id_hebergement = id_hebergement
        self.date_arrivee = date_arrivee
        self.date_depart = date_depart
        
class SeProduire(db.Model):
    __tablename__ = 'Se_Produire'
    id_groupe = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), primary_key=True)
    id_concert = db.Column(db.Integer, db.ForeignKey('Concert.id_concert'), primary_key=True)
    
    groupe = db.relationship('Groupe', backref=db.backref('se_produire_groupe', lazy=True))
    concert = db.relationship('Concert', backref=db.backref('Concert', lazy=True))
    
    def __init__(self, id_groupe, id_concert):
        self.id_groupe = id_groupe
        self.id_concert = id_concert
        
class FestivalLieu(db.Model):
    id_fest = db.Column(db.Integer, db.ForeignKey('Festival.id_fest'), primary_key=True)
    id_lieu = db.Column(db.Integer, db.ForeignKey('Lieu.id_lieu'), primary_key=True)
    
    festival = db.relationship('Festival', backref=db.backref('Festival', lazy=True))
    lieu = db.relationship('Lieu', backref=db.backref('festival_lieu_relation', lazy=True))
    
    def __init__(self, id_fest, id_lieu):
        self.id_fest = id_fest
        self.id_lieu = id_lieu
        
class ReseauxSociaux(db.Model):
    __tablename__ = 'Reseaux_Sociaux'
    id_reseaux_sociaux = db.Column(db.Integer, primary_key=True)
    nom_reseaux_sociaux = db.Column(db.String(50), nullable=False)
    url_reseaux_sociaux = db.Column(db.String(50), nullable=False)
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), nullable=False)
    
    groupe = db.relationship('Groupe', backref=db.backref('reseau_groupe_relation', lazy=True))
    
    def __init__(self, nom, url, id_group):
        self.nom_reseaux_sociaux = nom
        self.url_reseaux_sociaux = url
        self.id_group = id_group

class Photos(db.Model):
    __tablename__ = 'Photos'
    id_photos = db.Column(db.Integer, primary_key=True)
    url_photos = db.Column(db.String(50), nullable=False)
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), nullable=False)
    
    groupe = db.relationship('Groupe', backref=db.backref('photos_groupe_relation', lazy=True))
    
    def __init__(self, url, id_group):
        self.url_photos = url
        self.id_group = id_group
        
class Videos(db.Model):
    __tablename__ = 'Videos'
    id_videos = db.Column(db.Integer, primary_key=True)
    url_videos = db.Column(db.String(50), nullable=False)
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), nullable=False)
    
    groupe = db.relationship('Groupe', backref=db.backref('videos_groupe_relation', lazy=True))
    
    def __init__(self, url, id_group):
        self.url_videos = url
        self.id_group = id_group
        
def ajouter_festival(id_fest, nom, date_debut, duree):
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
    except Exception as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    
def ajouter_lieu(nom, adresse, ville, code_postal, pays, capacite, type_lieu):
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
    except Exception as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def ajouter_festival_lieu(id_fest, id_lieu):
    try :
        festival_lieu = FestivalLieu(id_fest, id_lieu)
        db.session.add(festival_lieu)
        db.session.commit()
        return f"Le festival {id_fest} a bien été ajouté au lieu {id_lieu}"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    except Exception as e:
        db.session.rollback()
        return "Erreur : " + str(e)

@login_manager.user_loader
def load_user() :
    return 1

