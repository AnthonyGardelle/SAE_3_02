-- Active: 1695737303069@@127.0.0.1@3306@sae_3_02
CREATE TABLE ACTIVITE (
  id_Activite INT NOT NULL UNIQUE,
  nom_Activite VARCHAR(42),
  statut VARCHAR(42),
  date_Debut_Activite TIMESTAMP,
  duree_Activite INT,
  PRIMARY KEY (id_Activite)
);

CREATE TABLE ARTISTE (
  id_Artiste INT NOT NULL UNIQUE,
  nom_Artiste VARCHAR(42),
  prenom_Artiste VARCHAR(42),
  instrument VARCHAR(42),
  id_Groupe INT NOT NULL,
  PRIMARY KEY (id_Artiste)
);

CREATE TABLE BILLET (
  id_Billet INT NOT NULL UNIQUE,
  duree_Billet INT,
  id_Festival INT NOT NULL,
  id_Spectateur INT NOT NULL,
  PRIMARY KEY (id_Billet)
);

CREATE TABLE CONCERT (
  id_Concert INT NOT NULL UNIQUE,
  nom_Concert VARCHAR(42),
  date_Debut_Concert TIMESTAMP,
  duree_Concert INT,
  temps_Montage INT,
  temps_Demontage INT,
  PRIMARY KEY (id_Concert)
);

CREATE TABLE FESTIVAL (
  id_Festival INT NOT NULL UNIQUE,
  nom_Festival VARCHAR(42),
  date_Debut_Festival TIMESTAMP,
  duree_Festival INT,
  id_Lieux INT NOT NULL,
  PRIMARY KEY (id_Festival)
);

CREATE TABLE GENRE_MUSICAL (
  id_Genre  INT NOT NULL UNIQUE,
  nom_Genre VARCHAR(42),
  PRIMARY KEY (id_Genre)
);

CREATE TABLE GROUPE (
  id_Groupe INT NOT NULL UNIQUE,
  nom_Groupe VARCHAR(42),
  description VARCHAR(42),
  photos VARCHAR(42),
  reseaux VARCHAR(42),
  video VARCHAR(42),
  id_Genre INT NOT NULL,
  PRIMARY KEY (id_Groupe)
);

CREATE TABLE HEBERGEMENT (
  id_Hebergement INT NOT NULL UNIQUE,
  nom_Hebergement VARCHAR(42),
  nb_Place_Par_Jour INT,
  PRIMARY KEY (id_Hebergement)
);

CREATE TABLE LIEUX (
  id_Lieux INT NOT NULL UNIQUE,
  nom_Lieux VARCHAR(42),
  type_Lieux VARCHAR(42),
  capacite INT,
  PRIMARY KEY (id_Lieux)
);

CREATE TABLE ORGANISE (
  id_Activite INT NOT NULL,
  id_Lieux INT NOT NULL,
  PRIMARY KEY (id_Activite, id_Lieux)
);

CREATE TABLE PARTICIPER (
  id_Groupe INT NOT NULL,
  id_Activite INT NOT NULL,
  PRIMARY KEY (id_Groupe, id_Activite)
);

CREATE TABLE SE_LOGER (
  id_Groupe INT NOT NULL,
  id_Hebergement INT NOT NULL,
  PRIMARY KEY (id_Groupe, id_Hebergement)
);

CREATE TABLE SE_PRODUIRE (
  id_Groupe INT NOT NULL,
  id_Concert INT NOT NULL,
  PRIMARY KEY (id_Groupe, id_Concert)
);

CREATE TABLE SPECTATEUR (
  id_Spectateur INT NOT NULL,
  nom_Spectateur VARCHAR(42),
  prenom_Spectateur VARCHAR(42),
  PRIMARY KEY (id_Spectateur)
);

CREATE TABLE STYLE_MUSICAL (
  id_Style INT NOT NULL,
  nom_Style VARCHAR(42),
  id_Genre INT NOT NULL,
  PRIMARY KEY (id_Style)
);

ALTER TABLE ARTISTE ADD FOREIGN KEY (id_Groupe) REFERENCES GROUPE (id_Groupe);

ALTER TABLE BILLET ADD FOREIGN KEY (id_Spectateur) REFERENCES SPECTATEUR (id_Spectateur);

ALTER TABLE BILLET ADD FOREIGN KEY (id_Festival) REFERENCES FESTIVAL (id_Festival);

ALTER TABLE FESTIVAL ADD FOREIGN KEY (id_Lieux) REFERENCES LIEUX (id_Lieux);

ALTER TABLE GROUPE ADD FOREIGN KEY (id_Genre) REFERENCES GENRE_MUSICAL (id_Genre);

ALTER TABLE ORGANISE ADD FOREIGN KEY (id_Lieux) REFERENCES LIEUX (id_Lieux);

ALTER TABLE ORGANISE ADD FOREIGN KEY (id_Activite) REFERENCES ACTIVITE (id_Activite);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (id_Activite) REFERENCES ACTIVITE (id_Activite);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (id_Groupe) REFERENCES GROUPE (id_Groupe);

ALTER TABLE SE_LOGER ADD FOREIGN KEY (id_Hebergement) REFERENCES HEBERGEMENT (id_Hebergement);

ALTER TABLE SE_LOGER ADD FOREIGN KEY (id_Groupe) REFERENCES GROUPE (id_Groupe);

ALTER TABLE SE_PRODUIRE ADD FOREIGN KEY (id_Concert) REFERENCES CONCERT (id_Concert);

ALTER TABLE SE_PRODUIRE ADD FOREIGN KEY (id_Groupe) REFERENCES GROUPE (id_Groupe);

ALTER TABLE STYLE_MUSICAL ADD FOREIGN KEY (id_Genre) REFERENCES GENRE_MUSICAL (id_Genre);

CREATE INDEX idx_id_Activite ON ACTIVITE (id_Activite);

CREATE INDEX idx_id_Artiste ON ARTISTE (id_Artiste);

CREATE INDEX idx_id_Billet ON BILLET (id_Billet);

CREATE INDEX idx_id_Concert ON CONCERT (id_Concert);

CREATE INDEX idx_id_Festival ON FESTIVAL (id_Festival);

CREATE INDEX idx_id_Genre ON GENRE_MUSICAL (id_Genre);

CREATE INDEX idx_id_Groupe ON GROUPE (id_Groupe);

CREATE INDEX idx_id_Hebergement ON HEBERGEMENT (id_Hebergement);

CREATE INDEX idx_id_Lieux ON LIEUX (id_Lieux);

CREATE INDEX idx_id_Spectateur ON SPECTATEUR (id_Spectateur);

CREATE INDEX idx_id_Style ON STYLE_MUSICAL (id_Style);

CREATE INDEX idx_id_Activite_id_Lieux ON ORGANISE (id_Activite, id_Lieux);

CREATE INDEX idx_id_Activite_id_Groupe ON PARTICIPER (id_Activite, id_Groupe);

CREATE INDEX idx_id_Groupe_id_Hebergement ON SE_LOGER (id_Groupe, id_Hebergement);

CREATE INDEX idx_id_Groupe_id_Concert ON SE_PRODUIRE (id_Groupe, id_Concert);

DELIMITER |
CREATE TRIGGER CheckConcertTiming
BEFORE INSERT ON CONCERT
FOR EACH ROW
BEGIN
  DECLARE lastConcertEndTime TIMESTAMP;
  
  -- Trouver la date de fin du dernier concert
  SELECT MAX(date_Debut_Concert + INTERVAL duree_Concert + temps_Demontage MINUTE)
  INTO lastConcertEndTime
  FROM CONCERT;
  
  IF NEW.date_Debut_Concert < lastConcertEndTime THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Le nouveau concert doit commencer après le dernier concert + temps de démontage.';
  END IF;
END |
DELIMITER ;