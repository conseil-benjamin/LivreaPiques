import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { useTranslation } from "react-i18next";
import Banner from "../../components/Banner/Banner.jsx";
import { CircularProgress } from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { Button } from "@mui/material"; // Pour le bouton de like
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';  // Cœur vide
import FavoriteIcon from '@mui/icons-material/Favorite';  // Cœur plein
import "./BookDetails.css";
import i18n from "i18next";
import { translateText } from "../../utils/translate.js";
import Cookies from "js-cookie";
import Swal from "sweetalert2";

function BookDetails() {
    const { book_id } = useParams();
    const [book, setBook] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { t } = useTranslation();
    const userId = Cookies.get("user_id"); // ID de l'utilisateur pour lier l'action
    const [isLiked, setIsLiked] = useState(false); // Etat pour savoir si l'utilisateur a liké le livre

    useEffect(() => {
        const fetchBookDetails = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/api/books/${book_id}`);
                if (response.data && response.data.length > 0) {
                    setBook(response.data[0]);
                } else {
                    setError(t("book_not_found"));
                }
            } catch (error) {
                setError(t("error_fetching"));
            } finally {
                setLoading(false);
            }
        };

        const checkIfLiked = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/api/likedbook/${userId}/${book_id}`);
                if (response.data.liked) {
                    setIsLiked(true); // Le livre est liké
                } else {
                    setIsLiked(false); // Le livre n'est pas liké
                }
            } catch (error) {
                console.error("Erreur lors de la vérification du like", error);
                setError(t("error_fetching"));
            }
        };

        if (userId) {
            checkIfLiked(); // Vérifie si l'utilisateur a liké ce livre
        }
        fetchBookDetails(); // Charge les détails du livre
    }, [book_id, userId, t]);

    // Fonction pour liker ou supprimer un like
    const handleLikeToggle = async (bookId) => {
        try {
            if (isLiked) {
                // Si déjà liké, supprimer le like
                await axios.delete(`http://localhost:8000/api/user/${userId}/like/${bookId}`);
                setIsLiked(false); // Met à jour l'état immédiatement
                await Swal.fire({
                    icon: "success",
                    title: t("unliked_book"),
                    showConfirmButton: false,
                    timer: 1500,
                    timerProgressBar: true,
                    toast: true,
                    position: "top-end",
                });
            } else {
                // Si non liké, ajouter le like
                await axios.post(`http://localhost:8000/api/likedbook/`, { user_id: userId,book_id: bookId });
                setIsLiked(true); // Met à jour l'état immédiatement
                await Swal.fire({
                    icon: "success",
                    title: t("liked_book"),
                    showConfirmButton: false,
                    timer: 1500,
                    timerProgressBar: true,
                    toast: true,
                    position: "top-end",
                });
            }
        } catch (error) {
            console.error("Erreur lors de la gestion du like", error);
        }
    };

    function splitText(text, maxLength) {
        const parts = [];
        let index = 0;
        while (index < text.length) {
            parts.push(text.substring(index, index + maxLength));
            index += maxLength;
        }
        return parts;
    }

    const [translatedDesc, setTranslatedDesc] = useState(book?.book_description || "");
    const [translatedTitle, setTranslatedTitle] = useState(book?.book_title || "");
    const [translatedGenres, setTranslatedGenres] = useState(book?.genres || "");
    const [isTranslating, setIsTranslating] = useState(false);

    useEffect(() => {
        if (book) {
            // Traduction de la description
            if (book.book_description) {
                if (i18n.language === "fr") {
                    setIsTranslating(true);
                    const parts = splitText(book.book_description, 500);
                    Promise.all(parts.map((part) => translateText(part, "fr")))  // Utilisation de LibreTranslate
                        .then((translations) => {
                            setTranslatedDesc(translations.join(" "));
                            setIsTranslating(false);
                        })
                        .catch(() => {
                            setTranslatedDesc(book.book_description);
                            setIsTranslating(false);
                        });
                } else {
                    setTranslatedDesc(book.book_description);
                }
            }

            // Traduction du titre
            if (book.book_title) {
                if (i18n.language === "fr") {
                    translateText(book.book_title, "fr")  // Utilisation de LibreTranslate
                        .then(setTranslatedTitle)
                        .catch(() => setTranslatedTitle(book.book_title));
                } else {
                    setTranslatedTitle(book.book_title);
                }
            }

            // Traduction des genres
            if (book.genres) {
                if (i18n.language === "fr") {
                    translateText(book.genres, "fr")  // Utilisation de LibreTranslate
                        .then(setTranslatedGenres)
                        .catch(() => setTranslatedGenres(book.genres));
                } else {
                    setTranslatedGenres(book.genres);
                }
            }
        }
    }, [i18n.language, book]);

    if (loading) {
        return (
            <div className="loading-container">
                <CircularProgress color="primary" />
                <p>{t("loading")}</p>
            </div>
        );
    }

    if (error) {
        return <div className="error-message">{error}</div>;
    }

    return (
        <>
            <div className="book-details-page">
                <ArrowBackIcon
                    className="back-icon"
                    onClick={() => navigate(-1)}
                    fontSize="large"
                />
                <div className="book-card">
                    <img
                        src={book.book_cover || "default-cover.jpg"}
                        alt={book.book_title}
                        className="book-cover"
                    />
                    <div className="book-info">
                        <h1>{translatedTitle ? translatedTitle : t("unknown")}</h1>
                        <p className="author">
                            {t("book_author")}: {book.authors || t("unknown")}
                        </p>
                        <p>
                            <strong>{t("book_genres")}</strong>: {translatedGenres || t("no_genres")}
                        </p>
                        <p className="description">
                            <strong>{t("book_description")}</strong>: {translatedDesc ? translatedDesc : book.book_description || t("no_description")}
                        </p>
                        <p>
                            <strong>{t("book_avg_rating")}</strong>: ⭐ {book.book_avg_rating || t("not_rated")}
                        </p>
                        <div
                            className="like-button"
                            onClick={() => handleLikeToggle(book.book_id)}
                            style={{ cursor: "pointer", color: isLiked ? "red" : "gray" }}
                        >
                            {isLiked ? <FavoriteIcon fontSize="large" /> : <FavoriteBorderIcon fontSize="large" />}
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}

export default BookDetails;
