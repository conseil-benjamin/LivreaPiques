-- Création de l'utilisateur admin avec tous les droits
CREATE ROLE admin WITH LOGIN PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE db_livreapique TO admin;

-- Création du rôle utilisateur
CREATE ROLE utilisateur;

-- Accorder les droits en lecture, insertion et mise à jour sur la table user et ses tables associées
GRANT SELECT, INSERT, UPDATE ON TABLE "user" TO utilisateur;
GRANT SELECT, INSERT, UPDATE ON TABLE User_Book_Source TO utilisateur;
GRANT SELECT, INSERT, UPDATE ON TABLE Fav_Medias TO utilisateur;
GRANT SELECT, INSERT, UPDATE ON TABLE Liked_Publisher TO utilisateur;
GRANT SELECT, INSERT, UPDATE ON TABLE Liked_Genres TO utilisateur;
GRANT SELECT, INSERT, UPDATE ON TABLE Liked_Series TO utilisateur;
GRANT SELECT, INSERT, UPDATE ON TABLE Liked_Author TO utilisateur;
GRANT SELECT, INSERT, UPDATE ON TABLE Liked_Books TO utilisateur;
GRANT SELECT, INSERT, UPDATE ON TABLE Fav_Books TO utilisateur;
GRANT SELECT, INSERT, UPDATE ON TABLE Reads_With TO utilisateur;

-- Restreindre les utilisateurs à n'accéder qu'à leurs propres données
REVOKE ALL ON TABLE "user" FROM PUBLIC;
ALTER TABLE "user" ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_isolation ON "user"
    USING (user_id = current_setting('app.current_user_id')::INTEGER);

-- Appliquer la politique de sécurité
ALTER TABLE "user" FORCE ROW LEVEL SECURITY;

-- Ajouter une fonction pour définir l'utilisateur courant
CREATE OR REPLACE FUNCTION set_current_user_id(uid INTEGER) RETURNS void AS $$
BEGIN
    PERFORM set_config('app.current_user_id', uid::TEXT, false);
END;
$$ LANGUAGE plpgsql;

-- Attribuer le rôle utilisateur par défaut à tous les utilisateurs
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE ON TABLE "user" TO utilisateur;

-- Insérer un utilisateur admin dans la table "user"
INSERT INTO "user" (username, password)
VALUES ('admin', 'admin');