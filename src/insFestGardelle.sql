-- Active: 1695737303069@@127.0.0.1@3306@sae_3_02
INSERT INTO GROUPE (id_Groupe,nom_Groupe,description,photos,reseaux,video,id_Genre) VALUES (
    1,'Groupe 1','Description 1','Photos 1','Reseaux 1','Video 1',1),
    (2,'Groupe 2','Description 2','Photos 2','Reseaux 2','Video 2',2),
    (3,'Groupe 3','Description 3','Photos 3','Reseaux 3','Video 3',3),
    (4,'Groupe 4','Description 4','Photos 4','Reseaux 4','Video 4',4),
    (5,'Groupe 5','Description 5','Photos 5','Reseaux 5','Video 5',5),
    (6,'Groupe 6','Description 6','Photos 6','Reseaux 6','Video 6',6),
    (7,'Groupe 7','Description 7','Photos 7','Reseaux 7','Video 7',7),
    (8,'Groupe 8','Description 8','Photos 8','Reseaux 8','Video 8',8),
    (9,'Groupe 9','Description 9','Photos 9','Reseaux 9','Video 9',9),
    (10,'Groupe 10','Description 10','Photos 10','Reseaux 10','Video 10',10);

INSERT INTO GENRE_MUSICAL (id_Genre,nom_Genre) VALUES (
    1,'Genre 1'),
    (2,'Genre 2'),
    (3,'Genre 3'),
    (4,'Genre 4'),
    (5,'Genre 5'),
    (6,'Genre 6'),
    (7,'Genre 7'),
    (8,'Genre 8'),
    (9,'Genre 9'),
    (10,'Genre 10');

INSERT INTO STYLE_MUSICAL (id_Style,nom_Style,id_Genre) VALUES (
    1,'Style 1',1),
    (2,'Style 2',2),
    (3,'Style 3',3),
    (4,'Style 4',4),
    (5,'Style 5',5),
    (6,'Style 6',6),
    (7,'Style 7',7),
    (8,'Style 8',8),
    (9,'Style 9',9),
    (10,'Style 10',10);

INSERT INTO SPECTATEUR (id_Spectateur,nom_Spectateur,prenom_Spectateur) VALUES (
    1,'Spectateur 1','Prenom 1'),
    (2,'Spectateur 2','Prenom 2'),
    (3,'Spectateur 3','Prenom 3'),
    (4,'Spectateur 4','Prenom 4'),
    (5,'Spectateur 5','Prenom 5'),
    (6,'Spectateur 6','Prenom 6'),
    (7,'Spectateur 7','Prenom 7'),
    (8,'Spectateur 8','Prenom 8'),
    (9,'Spectateur 9','Prenom 9'),
    (10,'Spectateur 10','Prenom 10');

INSERT INTO LIEUX (id_Lieux,nom_Lieux,type_Lieux,capacite) VALUES (
    1,'Lieux 1','Type 1',1),
    (2,'Lieux 2','Type 2',2),
    (3,'Lieux 3','Type 3',3),
    (4,'Lieux 4','Type 4',4),
    (5,'Lieux 5','Type 5',5),
    (6,'Lieux 6','Type 6',6),
    (7,'Lieux 7','Type 7',7),
    (8,'Lieux 8','Type 8',8),
    (9,'Lieux 9','Type 9',9),
    (10,'Lieux 10','Type 10',10);

INSERT INTO HEBERGEMENT (id_Hebergement,nom_Hebergement,nb_Place_Par_Jour) VALUES (
    1,'Hebergement 1',1),
    (2,'Hebergement 2',2),
    (3,'Hebergement 3',3),
    (4,'Hebergement 4',4),
    (5,'Hebergement 5',5),
    (6,'Hebergement 6',6),
    (7,'Hebergement 7',7),
    (8,'Hebergement 8',8),
    (9,'Hebergement 9',9),
    (10,'Hebergement 10',10);

INSERT INTO CONCERT (id_Concert,nom_Concert,date_Debut_Concert,duree_Concert,temps_Montage,temps_Demontage) VALUES (
    1,'Concert 1','2019-01-01 00:00:00',1,1,1),
    (2,'Concert 2','2019-01-02 00:00:00',2,2,2),
    (3,'Concert 3','2019-01-03 00:00:00',3,3,3),
    (4,'Concert 4','2019-01-04 00:00:00',4,4,4),
    (5,'Concert 5','2019-01-05 00:00:00',5,5,5),
    (6,'Concert 6','2019-01-06 00:00:00',6,6,6),
    (7,'Concert 7','2019-01-07 00:00:00',7,7,7),
    (8,'Concert 8','2019-01-08 00:00:00',8,8,8),
    (9,'Concert 9','2019-01-09 00:00:00',9,9,9),
    (10,'Concert 10','2019-01-10 00:00:00',10,10,10);

INSERT INTO FESTIVAL (id_Festival,nom_Festival,date_Debut_Festival,duree_Festival,id_Lieux) VALUES (
    1,'Festival 1','2019-01-01 00:00:00',1,1),
    (2,'Festival 2','2019-01-02 00:00:00',2,2),
    (3,'Festival 3','2019-01-03 00:00:00',3,3),
    (4,'Festival 4','2019-01-04 00:00:00',4,4),
    (5,'Festival 5','2019-01-05 00:00:00',5,5),
    (6,'Festival 6','2019-01-06 00:00:00',6,6),
    (7,'Festival 7','2019-01-07 00:00:00',7,7),
    (8,'Festival 8','2019-01-08 00:00:00',8,8),
    (9,'Festival 9','2019-01-09 00:00:00',9,9),
    (10,'Festival 10','2019-01-10 00:00:00',10,10);

INSERT INTO BILLET (id_Billet,duree_Billet,id_Festival,id_Spectateur) VALUES (
    1,1,1,1),
    (2,2,2,2),
    (3,3,3,3),
    (4,4,4,4),
    (5,5,5,5),
    (6,6,6,6),
    (7,7,7,7),
    (8,8,8,8),
    (9,9,9,9),
    (10,10,10,10);

INSERT INTO ACTIVITE (id_Activite,nom_Activite,statut,date_Debut_Activite,duree_Activite) VALUES (
    1,'Activite 1','Statut 1','2019-01-01 00:00:00',1),
    (2,'Activite 2','Statut 2','2019-01-02 00:00:00',2),
    (3,'Activite 3','Statut 3','2019-01-03 00:00:00',3),
    (4,'Activite 4','Statut 4','2019-01-04 00:00:00',4),
    (5,'Activite 5','Statut 5','2019-01-05 00:00:00',5),
    (6,'Activite 6','Statut 6','2019-01-06 00:00:00',6),
    (7,'Activite 7','Statut 7','2019-01-07 00:00:00',7),
    (8,'Activite 8','Statut 8','2019-01-08 00:00:00',8),
    (9,'Activite 9','Statut 9','2019-01-09 00:00:00',9),
    (10,'Activite 10','Statut 10','2019-01-10 00:00:00',10);

INSERT INTO ARTISTE (id_Artiste,nom_Artiste,prenom_Artiste,instrument,id_Groupe) VALUES (
    1,'Artiste 1','Prenom 1','Instrument 1',1),
    (2,'Artiste 2','Prenom 2','Instrument 2',2),
    (3,'Artiste 3','Prenom 3','Instrument 3',3),
    (4,'Artiste 4','Prenom 4','Instrument 4',4),
    (5,'Artiste 5','Prenom 5','Instrument 5',5),
    (6,'Artiste 6','Prenom 6','Instrument 6',6),
    (7,'Artiste 7','Prenom 7','Instrument 7',7),
    (8,'Artiste 8','Prenom 8','Instrument 8',8),
    (9,'Artiste 9','Prenom 9','Instrument 9',9),
    (10,'Artiste 10','Prenom 10','Instrument 10',10);

INSERT INTO ORGANISE (id_Activite, id_Lieux) VALUES (
    1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    (6,6),
    (7,7),
    (8,8),
    (9,9),
    (10,10);

INSERT INTO PARTICIPER (id_Groupe,id_Activite) VALUES (
    1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    (6,6),
    (7,7),
    (8,8),
    (9,9),
    (10,10);

INSERT INTO SE_LOGER (id_Groupe,id_Hebergement) VALUES (
    1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    (6,6),
    (7,7),
    (8,8),
    (9,9),
    (10,10);

INSERT INTO SE_PRODUIRE (id_Groupe,id_Concert) VALUES (
    1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    (6,6),
    (7,7),
    (8,8),
    (9,9),
    (10,10);