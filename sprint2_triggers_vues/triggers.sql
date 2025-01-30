-- Trois livres préférés
CREATE OR REPLACE FUNCTION check_user_book_limit()
RETURNS TRIGGER AS $$
DECLARE
    fav_count INT;
BEGIN
    SELECT COUNT(*) INTO fav_count
    FROM public.fav_books
    WHERE user_id = NEW.user_id;

    IF fav_count >= 3 THEN
        RAISE EXCEPTION 'Un utilisateur ne peux avoir que trois médias favoris.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_user_book_limit
BEFORE INSERT ON public.fav_books
FOR EACH ROW
EXECUTE FUNCTION check_user_book_limit();

-- Media favoris
CREATE OR REPLACE FUNCTION check_one_media_per_user()
RETURNS TRIGGER AS $$
DECLARE
    media_count INT;
BEGIN
    SELECT COUNT(*) INTO media_count
    FROM fav_medias
    WHERE user_id = NEW.user_id;

    IF media_count >= 1 THEN
        RAISE EXCEPTION 'Un user ne peut avoir qu un seul média préféré.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER trg_check_one_media_per_user
BEFORE INSERT ON fav_medias
FOR EACH ROW
EXECUTE FUNCTION check_one_media_per_user();
