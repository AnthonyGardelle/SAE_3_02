-- Insertion de données dans la table GENRE_MUSICAL
INSERT INTO GENRE_MUSICAL (id_Genre,nom_Genre) VALUES 
(1,'Musique du Monde'),
(2,'Rock'),
(3,'Jazz'),
(4,'Ambient'),
(5,'Fusion'),
(6,'Chœur'),
(7,'Musique Latine'),
(8,'Folk'),
(9,'Électronique'),
(10,'Hip-Hop');

-- Insertion de données dans la table GROUPE
INSERT INTO GROUPE (id_Groupe,nom_Groupe,description,photos,reseaux,video,id_Genre) VALUES 
(1,'Les Mélodies du Monde','Groupe de musique du monde','melodies.jpg','@melodies_monde','video_melodies',1),
(2,'Rock Éternel','Groupe de rock classique','rock.jpg','@rock_eternel','video_rock',2),
(3,'Jazz Harmonie','Ensemble de jazz instrumental','jazz.jpg','@jazz_harmonie','video_jazz',3),
(4,'Sons de la Nature','Groupe de musique ambient','ambient.jpg','@sons_nature','video_ambient',4),
(5,'Fusion Urbaine','Groupe de fusion urbaine','fusion.jpg','@fusion_urbaine','video_fusion',5),
(6,'Voix Célestes','Chœur a cappella','choeur.jpg','@voix_celestes','video_choeur',6),
(7,'Rythmes Latins','Groupe de musique latine','latino.jpg','@rythmes_latins','video_latino',7),
(8,'Mélodies Folkloriques','Groupe de musique folk','folk.jpg','@melodies_folk','video_folk',8),
(9,'Sons Électroniques','Musique électronique expérimentale','electronique.jpg','@sons_electroniques','video_electronique',9),
(10,'Hip-Hop Harmonique','Groupe de hip-hop créatif','hiphop.jpg','@hiphop_harmonique','video_hiphop',10);

-- Insertion de données dans la table STYLE_MUSICAL
INSERT INTO STYLE_MUSICAL (id_Style,nom_Style,id_Genre) VALUES 
(1,'Traditionnel','1'),
(2,'Classique','2'),
(3,'Smooth Jazz','3'),
(4,'Chillout','4'),
(5,'Jazz-Funk','3'),
(6,'Pop-Fusion','5'),
(7,'Salsa','7'),
(8,'Country','8'),
(9,'House','9'),
(10,'Rap','10');

-- Insertion de données dans la table SPECTATEUR
INSERT INTO SPECTATEUR (id_Spectateur,nom_Spectateur,prenom_Spectateur) VALUES 
(1,'Martin','Pierre'),
(2,'Dupuis','Sophie'),
(3,'Lefebvre','Claire'),
(4,'Gagné','Michel'),
(5,'Lavoie','Émilie'),
(6,'Rivard','Marc'),
(7,'Bergeron','Julie'),
(8,'Bouchard','Luc'),
(9,'Pelletier','Catherine'),
(10,'Girard','Sylvie');

-- Insertion de données dans la table LIEUX
INSERT INTO LIEUX (id_Lieux,nom_Lieux,type_Lieux,capacite) VALUES 
(1,'Salle de Concert A','Salle de Concert',1000),
(2,'Stade Municipal','Stade',5000),
(3,'Club de Jazz Central','Club de Jazz',150),
(4,'Théâtre Communal','Théâtre',300),
(5,'Espace Culturel','Salle Polyvalente',800),
(6,'Bar Musical Le Coin','Bar Musical',80),
(7,'Amphithéâtre en Plein Air','Amphithéâtre',2000),
(8,'Salle des Fêtes','Salle des Fêtes',400),
(9,'Salle de Spectacle Intime','Salle de Spectacle',120),
(10,'Salle de Danse Latino','Salle de Danse',50);

-- Insertion de données dans la table HEBERGEMENT
INSERT INTO HEBERGEMENT (id_Hebergement,nom_Hebergement,nb_Place_Par_Jour) VALUES 
(1,'Hôtel Étoile','100'),
(2,'Auberge du Centre','50'),
(3,'Motel Charmant','30'),
(4,'Pension du Voyageur','20'),
(5,'Chambre d\'Hôte Paisible','10'),
(6,'Gîte Champêtre','15'),
(7,'Chalet Montagnard','8'),
(8,'Résidence Étudiante','200'),
(9,'Auberge de Jeunesse','70'),
(10,'Gîte de Luxe','5');

-- Insertion de données dans la table CONCERT
INSERT INTO CONCERT (id_Concert,nom_Concert,date_Debut_Concert,duree_Concert,temps_Montage,temps_Demontage) VALUES 
(1,'Concert d\'Ouverture','2023-01-15 19:00:00',3,2,1),
(2,'Rock Fest','2023-01-16 18:30:00',4,2,2),
(3,'Jazz Night','2023-01-17 20:00:00',3,1,1),
(4,'Ambient Sounds','2023-01-18 21:00:00',2,1,1),
(5,'Fusion Groove','2023-01-19 19:30:00',3,2,1),
(6,'Voix en Harmonie','2023-01-20 20:00:00',2,1,1),
(7,'Salsa Fever','2023-01-21 22:00:00',3,1,1),
(8,'Folk Stories','2023-01-22 18:00:00',4,2,2),
(9,'Electro Beats','2023-01-23 21:30:00',3,1,1),
(10,'Hip-Hop Showcase','2023-01-24 20:30:00',2,1,1);

-- Insertion de données dans la table FESTIVAL
INSERT INTO FESTIVAL (id_Festival,nom_Festival,date_Debut_Festival,duree_Festival,id_Lieux) VALUES 
(1,'Festival de la Musique','2023-01-15 10:00:00',10,1),
(2,'RockFest 2023','2023-01-16 10:30:00',9,2),
(3,'JazzFest','2023-01-17 11:00:00',8,3),
(4,'Ambient Experience','2023-01-18 12:00:00',7,4),
(5,'Fusion Extravaganza','2023-01-19 12:30:00',6,5),
(6,'Harmonie Vocale','2023-01-20 13:00:00',5,6),
(7,'Fiesta Latina','2023-01-21 14:00:00',4,7),
(8,'Folklore Fest','2023-01-22 14:30:00',3,8),
(9,'Electro Vibes','2023-01-23 15:00:00',2,9),
(10,'Hip-Hop Revolution','2023-01-24 15:30:00',1,10);

-- Insertion de données dans la table BILLET
INSERT INTO BILLET (id_Billet,duree_Billet,id_Festival,id_Spectateur) VALUES 
(1,1,1,1),
(2,2,2,2),
(3,3,3,3),
(4,4,4,4),
(5,5,5,5),
(6,6,6,6),
(7,7,7,7),
(8,8,8,8),
(9,9,9,9),
(10,10,10,10);

-- Insertion de données dans la table ACTIVITE
INSERT INTO ACTIVITE (id_Activite,nom_Activite,statut,date_Debut_Activite,duree_Activite) VALUES 
(1,'Atelier de Musique du Monde','En Cours','2023-01-15 10:00:00',2),
(2,'Masterclass de Guitare Rock','Planifié','2023-01-16 11:00:00',3),
(3,'Session d\'Improvisation Jazz','Terminé','2023-01-17 14:00:00',1),
(4,'Séance de Relaxation Ambient','En Cours','2023-01-18 16:00:00',1),
(5,'Atelier de Fusion Musicale','Planifié','2023-01-19 14:30:00',2),
(6,'Répétition Chorale','Terminé','2023-01-20 17:00:00',1),
(7,'Cours de Danse Salsa','Planifié','2023-01-21 18:00:00',2),
(8,'Atelier de Musique Folk','En Cours','2023-01-22 14:00:00',3),
(9,'Séance d\'Écoute Électronique','Planifié','2023-01-23 16:30:00',1),
(10,'Atelier de Beatbox Hip-Hop','En Cours','2023-01-24 17:30:00',2);

-- Insertion de données dans la table ORGANISE
INSERT INTO ORGANISE (id_Activite, id_Lieux) VALUES 
(1,1),
(2,2),
(3,3),
(4,4),
(5,5),
(6,6),
(7,7),
(8,8),
(9,9),
(10,10);

-- Insertion de données dans la table PARTICIPER
INSERT INTO PARTICIPER (id_Groupe,id_Activite) VALUES 
(1,1),
(2,2),
(3,3),
(4,4),
(5,5),
(6,6),
(7,7),
(8,8),
(9,9),
(10,10);

-- Insertion de données dans la table SE_LOGER
INSERT INTO SE_LOGER (id_Groupe,id_Hebergement) VALUES 
(1,1),
(2,2),
(3,3),
(4,4),
(5,5),
(6,6),
(7,7),
(8,8),
(9,9),
(10,10);    

-- Insertion de données dans la table SE_PRODUIRE
INSERT INTO SE_PRODUIRE (id_Groupe,id_Concert) VALUES 
(1,1),
(2,2),
(3,3),
(4,4),
(5,5),
(6,6),
(7,7),
(8,8),
(9,9),
(10,10);