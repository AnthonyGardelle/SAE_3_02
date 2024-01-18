from .app import db, login_manager
from sqlalchemy import CheckConstraint
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from flask_login import UserMixin
from hashlib import sha256

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
    
    def __init__(self, id_fest, nom, date_debut, duree):
        self.id_fest = id_fest
        self.nom_fest = nom
        self.date_debut_fest = date_debut
        self.duree_fest = duree
        
    def to_dict(self):
        return {
            'id': self.id_fest,
            'nom': self.nom_fest,
            'date_debut': self.date_debut_fest,
            'duree': self.duree_fest,
        }

class Spectateur(db.Model, UserMixin) :
    __tablename__ = 'Spectateur'
    id_spectateur = db.Column(db.Integer, primary_key=True)
    nom_spectateur = db.Column(db.String(50), nullable=False)
    prenom_spectateur = db.Column(db.String(50), nullable=False)
    mot_de_passe_spectateur = db.Column(db.String(64), nullable=False)

    def __init__(self, nom, prenom, mot_de_passe):
        self.nom_spectateur = nom
        self.prenom_spectateur = prenom
        self.mot_de_passe_spectateur = mot_de_passe
    
    def to_dict(self):
        return {
            'id': self.id_spectateur,
            'nom': self.nom_spectateur,
            'prenom': self.prenom_spectateur,
            'mot_de_passe': self.mot_de_passe_spectateur,
        }

    def get_id(self):
        return self.id_spectateur
    
    def ajouter_favoris(self, id_group) :
        if not id_group:
            return "L'id du groupe ne peut pas être vide"
        try :
            favoris = Favoris(id_group, self.id_spectateur)
            db.session.add(favoris)
            db.session.commit()
            return f"Le groupe {id_group} a bien été ajouté aux favoris du spectateur {self.id_spectateur}"
        except IntegrityError as e:
            db.session.rollback()
            return "Erreur : " + str(e)
        except Exception as e:
            db.session.rollback()
            return "Erreur : " + str(e)
        
    def enlever_favoris(self, id_group) :
        if not id_group:
            return "L'id du groupe ne peut pas être vide"
        try :
            favoris = Favoris.query.filter_by(id_group=id_group, id_spectateur=self.id_spectateur).first()
            db.session.delete(favoris)
            db.session.commit()
            return f"Le groupe {id_group} a bien été enlevé des favoris du spectateur {self.id_spectateur}"
        except IntegrityError as e:
            db.session.rollback()
            return "Erreur : " + str(e)
        except Exception as e:
            db.session.rollback()
            return "Erreur : " + str(e)

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

    def get_photo(self):
        return Photos.query.filter_by(id_group=self.id_groupe).first()

    def get_genre(self):
        return GenreMusical.query.filter_by(id_genre_musical=self.id_genre_musical).first()

    def get_membres(self) :
        return Artiste.query.filter_by(id_groupe=self.id_groupe).all()
    
    def get_reseaux(self) :
        return ReseauxSociaux.query.filter_by(id_group=self.id_groupe).all()
    
    def est_favoris(self, id_spectateur) :
        return Favoris.query.filter_by(id_group=self.id_groupe, id_spectateur=id_spectateur).first() is not None
    
    def get_nb_membres(self) :
        return len(self.get_membres())
    
    def get_concerts(self) :
        return SeProduire.query.filter_by(id_groupe=self.id_groupe).all()

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
    id_billet = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_spectateur = db.Column(db.Integer, db.ForeignKey('Spectateur.id_spectateur'), nullable=False)
    id_fest = db.Column(db.Integer, db.ForeignKey('Festival.id_fest'), nullable=False)
    id_type_billet = db.Column(db.String(50), db.ForeignKey('Type_Billet.id_type_billet'), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)

    spectateur = db.relationship('Spectateur', backref='billets', lazy=True)
    festival = db.relationship('Festival', backref='billets', lazy=True)

    __table_args__ = (
        CheckConstraint('id_spectateur > 0'),
        CheckConstraint('id_fest > 0'),
    )

    def __init__(self, id_spectateur, id_festival, id_type_billet, date_debut):
        self.id_spectateur = id_spectateur
        self.id_fest = id_festival
        self.id_type_billet = id_type_billet
        self.date_debut = date_debut
        
    def to_dict(self):
        return {
            'id': self.id_billet,
            'id_spectateur': self.id_spectateur,
            'id_festival': self.id_fest,
            'id_type_billet': self.id_type_billet,
            'festival': self.festival.to_dict() if self.festival else None,
            'spectateur': self.spectateur.to_dict() if self.spectateur else None,
            'date_debut': self.date_debut,
        }
        
class TypeBillet(db.Model):
    __tablename__ = 'Type_Billet'
    id_type_billet = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_type_billet = db.Column(db.String(50))
    duree_validite_type_billet = db.Column(db.Integer, nullable=False)
    prix_type_billet = db.Column(db.Float, nullable=False)
    quantite_initiale_disponible_type_billet = db.Column(db.Integer, nullable=False)

    billets = db.relationship('Billet', backref='type_billet', lazy=True)

    def __init__(self, nom, duree_validite, prix, quantite_initiale_disponible):
        self.nom_type_billet = nom
        self.duree_validite_type_billet = duree_validite
        self.prix_type_billet = prix
        self.quantite_initiale_disponible_type_billet = quantite_initiale_disponible
        
    def to_dict(self):
        return {
            'id': self.id_type_billet,
            'nom': self.nom_type_billet,
            'duree': self.duree_validite_type_billet,
            'prix': self.prix_type_billet,
            'quantite_dispo': self.quantite_initiale_disponible_type_billet,
            'quantite_reservee': len(self.billets) if self.billets else 0,
        }
    
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

class Favoris(db.Model):
    __tablename__ = 'Favoris'
    id_favoris = db.Column(db.Integer, primary_key=True)
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), nullable=False)
    id_spectateur = db.Column(db.Integer, db.ForeignKey('Spectateur.id_spectateur'), nullable=False)

    groupe = db.relationship('Groupe', backref=db.backref('favoris_groupe_relation', lazy=True))
    spectateur = db.relationship('Spectateur', backref=db.backref('favoris_spectateur_relation', lazy=True))

    def __init__(self, id_group, id_spectateur):
        self.id_group = id_group
        self.id_spectateur = id_spectateur

    def get_group(self):
        return Groupe.query.get(int(self.id_group))

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

def get_types_billets():
    types_billets = []
    for type_billet in TypeBillet.query.all():
        types_billets.append(type_billet.to_dict())
    return types_billets

def ajouter_type_billet(nom, duree_validite, prix, quantite_initiale_disponible):
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
    except Exception as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    
def ajouter_genre_musical(nom_genre_musical):
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
    
def get_jours_festival():
    jours_festival = []
    debut = Festival.query.first().date_debut_fest
    duree = Festival.query.first().duree_fest
    for i in range(duree):
        jours_festival.append(debut + timedelta(days=i))
    return jours_festival

def get_duree_fest():
    return Festival.query.first().duree_fest

def get_spectateur(nom, prebom):
    return Spectateur.query.filter_by(nom_spectateur=nom, prenom_spectateur=prebom).first()

def get_spect_by_id(id_spect):
    return Spectateur.query.filter_by(id_spectateur = id_spect).first()

def add_spectateur(nom, prenom):
    try :
        spectateur = Spectateur(nom, prenom)
        db.session.add(spectateur)
        db.session.commit()
        return f"Le spectateur {nom} {prenom} a bien été ajouté"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def add_billet(id_spect, id_festival, id_type_billet, date_debut):
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

def get_billet(id_spect, id_festival, id_type_billet, date_debut):
    return Billet.query.filter_by(id_spectateur=id_spect, id_fest=id_festival, id_type_billet=id_type_billet, date_debut=date_debut).first()

def get_activites():
    activites = []
    for activite in Activite.query.all():
        activites.append(activite)
    return activites

@login_manager.user_loader
def load_user() :
    return 1
    
def ajouter_groupe(nom_groupe, id_genre_musical) :
    if not nom_groupe:
        return "Le nom du groupe ne peut pas être vide"
    if not id_genre_musical:
        return "L'id du genre musical ne peut pas être vide"
    try :
        groupe = Groupe(nom_groupe, id_genre_musical)
        db.session.add(groupe)
        db.session.commit()
        return f"Le groupe {nom_groupe} a bien été ajouté"
    except IntegrityError as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    except Exception as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    
def ajouter_favoris(id_group, id_spectateur) :
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
    except Exception as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    
def ajouter_spectateur(nom_spectateur, prenom_spectateur, mot_de_passe_spectateur) :
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
    except Exception as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    
def ajouter_photos(url_photos, id_group) :
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
    except Exception as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def ajouter_artiste(nom_artiste, prenom_artiste, instrument_artiste, id_groupe) :
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
    except Exception as e:
        db.session.rollback()
        return "Erreur : " + str(e)
    
def ajouter_reseaux_sociaux(nom_reseaux_sociaux, url_reseaux_sociaux, id_group) :
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
    except Exception as e:
        db.session.rollback()
        return "Erreur : " + str(e)

def get_favoris_by_spec(id_spectateur) :
    return Favoris.query.filter_by(id_spectateur=id_spectateur).all()

def get_random_groupes() :
    return Groupe.query.order_by(db.func.random()).limit(10).distinct().all()

def get_group(id_group) :
    return Groupe.query.filter_by(id_groupe=id_group).first()

@login_manager.user_loader
def load_user(id_spectateur) :
    return Spectateur.query.get(int(id_spectateur))
