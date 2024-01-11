from .app import login_manager
from .app import db

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
    
    def __init__(self, nom, date_debut, duree):
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
    
    lieu = db.relationship('Lieu', backref=db.backref('Lieu', lazy=True))
    
    def __init__(self, nom, date_debut, duree, montage, demontage, id_lieu):
        self.nom_concert = nom
        self.date_debut_concert = date_debut
        self.duree_concert = duree
        self.temps_montage = montage
        self.temps_demontage = demontage
        self.id_lieu = id_lieu

class StyleMusical(db.Model):
    __tablename__ = 'Style_Musical'
    id_style_musical = db.Column(db.Integer, primary_key=True)
    nom_style_musical = db.Column(db.String(50), nullable=False)
    id_genre_musical = db.Column(db.Integer, db.ForeignKey('Genre_Musical.id_genre_musical'), nullable=False)
    
    genre_musical = db.relationship('GenreMusical', backref=db.backref('Genre_Musical', lazy=True))
    
    def __init__ (self, nom, id_genre_musical):
        self.nom_style_musical = nom
        self.id_genre_musical = id_genre_musical
        
class Billet(db.Model):
    __tablename__ = 'Billet'
    id_billet = db.Column(db.Integer, primary_key=True)
    prix_billet = db.Column(db.Float, nullable=False)
    duree_validite_billet = db.Column(db.Integer, nullable=False)
    id_spectateur = db.Column(db.Integer, db.ForeignKey('Spectateur.id_spectateur'), nullable=False)
    id_fest = db.Column(db.Integer, db.ForeignKey('Festival.id_fest'), nullable=False)
    
    spectateur = db.relationship('Spectateur', backref=db.backref('Spectateur', lazy=True))
    festival = db.relationship('Festival', backref=db.backref('Festival', lazy=True))
    
    def __init__(self, prix, duree, id_spectateur, id_fest):
        self.prix_billet = prix
        self.duree_validite_billet = duree
        self.id_spectateur = id_spectateur
        self.id_fest = id_fest
    
class Organise(db.Model):
    __tablename__ = 'Organise'
    id_activite = db.Column(db.Integer, db.ForeignKey('Activite.id_activite'), primary_key=True)
    id_lieu = db.Column(db.Integer, db.ForeignKey('Lieu.id_lieu'), primary_key=True)
    
    activite = db.relationship('Activite', backref=db.backref('Activite', lazy=True))
    lieu = db.relationship('Lieu', backref=db.backref('Lieu', lazy=True))
    
    def __init__(self, id_activite, id_lieu):
        self.id_activite = id_activite
        self.id_lieu = id_lieu

class Participer(db.Model):
    __tablename__ = 'Participer'
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), primary_key=True)
    id_activite = db.Column(db.Integer, db.ForeignKey('Activite.id_activite'), primary_key=True)
    
    groupe = db.relationship('Groupe', backref=db.backref('Groupe', lazy=True))
    activite = db.relationship('Activite', backref=db.backref('Activite', lazy=True))
    
    def __init__(self, id_groupe, id_activite):
        self.id_groupe = id_groupe
        self.id_activite = id_activite
        
class SeLoger(db.Model):
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), primary_key=True)
    id_hebergement = db.Column(db.Integer, db.ForeignKey('Hebergement.id_hebergement'), primary_key=True)
    date_arrivee = db.Column(db.Date, nullable=False)
    date_depart = db.Column(db.Date, nullable=False)
    
    groupe = db.relationship('Groupe', backref=db.backref('Groupe', lazy=True))
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
    
    groupe = db.relationship('Groupe', backref=db.backref('Groupe', lazy=True))
    concert = db.relationship('Concert', backref=db.backref('Concert', lazy=True))
    
    def __init__(self, id_groupe, id_concert):
        self.id_groupe = id_groupe
        self.id_concert = id_concert
        
class FestivalLieu(db.Model):
    id_fest = db.Column(db.Integer, db.ForeignKey('Festival.id_fest'), primary_key=True)
    id_lieu = db.Column(db.Integer, db.ForeignKey('Lieu.id_lieu'), primary_key=True)
    
    festival = db.relationship('Festival', backref=db.backref('Festival', lazy=True))
    lieu = db.relationship('Lieu', backref=db.backref('Lieu', lazy=True))
    
    def __init__(self, id_fest, id_lieu):
        self.id_fest = id_fest
        self.id_lieu = id_lieu
        
class ReseauxSociaux(db.Model):
    __tablename__ = 'Reseaux_Sociaux'
    id_reseaux_sociaux = db.Column(db.Integer, primary_key=True)
    nom_reseaux_sociaux = db.Column(db.String(50), nullable=False)
    url_reseaux_sociaux = db.Column(db.String(50), nullable=False)
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), nullable=False)
    
    groupe = db.relationship('Groupe', backref=db.backref('Groupe', lazy=True))
    
    def __init__(self, nom, url, id_artiste):
        self.nom_reseaux_sociaux = nom
        self.url_reseaux_sociaux = url
        self.id_artiste = id_artiste

class Photos(db.Model):
    __tablename__ = 'Photos'
    id_photos = db.Column(db.Integer, primary_key=True)
    url_photos = db.Column(db.String(50), nullable=False)
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), nullable=False)
    
    groupe = db.relationship('Groupe', backref=db.backref('Groupe', lazy=True))
    
    def __init__(self, url, id_artiste):
        self.url_photos = url
        self.id_artiste = id_artiste
        
class Videos(db.Model):
    __tablename__ = 'Videos'
    id_videos = db.Column(db.Integer, primary_key=True)
    url_videos = db.Column(db.String(50), nullable=False)
    id_group = db.Column(db.Integer, db.ForeignKey('Groupe.id_groupe'), nullable=False)
    
    groupe = db.relationship('Groupe', backref=db.backref('Groupe', lazy=True))
    
    def __init__(self, url, id_artiste):
        self.url_videos = url
        self.id_artiste = id_artiste

@login_manager.user_loader
def load_user() :
    return 1