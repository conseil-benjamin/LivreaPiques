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
import ImageUnvailable from "../../components/ImageUnvailable.jsx";
//Partie wishlist, les signets
import BookmarkBorderIcon from '@mui/icons-material/BookmarkBorder';
import BookmarkIcon from '@mui/icons-material/Bookmark';
import StarOutlineIcon from '@mui/icons-material/StarOutline'; // Etoile vide
import StarIcon from '@mui/icons-material/Star'; // Etoile pleine
import StarHalfIcon from '@mui/icons-material/StarHalf'; // Etoile à moitié pleine
//Partie Livres Lus
import AutoStoriesIcon from '@mui/icons-material/AutoStories'; // Filled version
import AutoStoriesOutlinedIcon from '@mui/icons-material/AutoStoriesOutlined'; // Hollow version

function BookDetails() {
    const { book_id } = useParams();
    const [book, setBook] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { t } = useTranslation();
    const userId = Cookies.get("user_id"); // ID de l'utilisateur pour lier l'action
    const [isLiked, setIsLiked] = useState(false); // Etat pour savoir si l'utilisateur a liké le livre
    const [isWishlisted, setIsWishlisted] = useState(false); // Etat pour savoir si l'utilisateur a ajouté le livre à sa wishlist
    const [isDescriptionExpanded, setIsDescriptionExpanded] = useState(false);
    const [isRead, setIsRead] = useState(false);
    const [userRating, setUserRating] = useState(0);
    const [hoveredRating, setHoveredRating] = useState(0);
    const toggleDescription = () => {
        setIsDescriptionExpanded(!isDescriptionExpanded);
    };

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

        const checkIfWishlisted = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/api/wishlist/${userId}/${book_id}`);
                setIsWishlisted(response.data.wishlisted);
            } catch (error) {
                console.error("Error checking wishlist status:", error);
            }
        };


        const checkIfRead = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/api/readbook/${userId}/${book_id}`);
                setIsRead(response.data.read);
            } catch (error) {
                console.error("Error checking read status:", error);
            }
        };

        const checkUserRating = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/api/books/${book_id}/rating/${userId}`);
                if (response.data && response.data.rating) {
                    setUserRating(response.data.rating);
                }
            } catch (error) {
                console.error("Error fetching user rating:", error);

            }
        };
    
        fetchBookDetails();
        if (userId) {
            checkIfLiked();
            checkIfWishlisted();

            checkIfRead();
            checkUserRating(); // Ajout de la vérification du rating

        }
    }, [book_id, userId, t]);

    // Fonction pour liker ou supprimer un like
    const handleLikeToggle = async (bookId) => {
        try {
            if (isLiked) {
                // Remove like
                await axios.delete(`http://localhost:8000/api/user/${userId}/like/${bookId}`);
                setIsLiked(false);
                await Swal.fire({
                    icon: "success",
                    title: t("unliked_book"),
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    toast: true,
                    position: "top-end",
                });
            } else {
                // Si le livre est dans la wishlist, le retirer d'abord
                if (isWishlisted) {
                    await axios.delete(`http://localhost:8000/api/user/${userId}/wishlist/${bookId}`);
                    setIsWishlisted(false);
                }
                // Si le livre est lu, le retirer d'abord
                if (isRead) {
                    await axios.delete(`http://localhost:8000/api/user/${userId}/read/${bookId}`);
                    setIsRead(false);
                }
                // ajouter le like
                await axios.post(`http://localhost:8000/api/likedbook/`, { 
                    user_id: userId,
                    book_id: bookId 
                });
                setIsLiked(true);
                await Swal.fire({
                    icon: "success",
                    title: isWishlisted ? t("Retiré de la liste de souhait et liké") : t("liked_book"),
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    toast: true,
                    position: "top-end",
                });
            }
        } catch (error) {
            console.error("Error handling like:", error);
            // ... error handling ...
        }
    };

    // Section pour la wishlist
    const checkIfWishlisted = async () => {
        try {
            const response = await axios.get(`http://localhost:8000/api/wishlist/${userId}/${book_id}`);
            setIsWishlisted(response.data.wishlisted);
        } catch (error) {
            console.error("Error checking wishlist status:", error);
        }
    };
    
    // if (userId) {
    //     checkIfLiked();
    //     checkIfWishlisted();
    // }

    // Add wishlist toggle handler
    const handleWishlistToggle = async (bookId) => {
        try {
            if (isWishlisted) {
                // Si déjà dans la wishlist, retirer
                await axios.delete(`http://localhost:8000/api/user/${userId}/wishlist/${bookId}`);
                setIsWishlisted(false); // Met à jour l'état immédiatement
                await Swal.fire({
                    icon: "success",
                    title: t("removed_from_wishlist"),
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    toast: true,
                    position: "top-end",
                });
            } else {
                // Vérifier si le livre est liké avant d'ajouter à la wishlist
                if (isLiked) {
                    await Swal.fire({
                        icon: "error",
                        title: t("cannot_wishlist_liked_book"),
                        showConfirmButton: false,
                        timer: 3000,
                        timerProgressBar: true,
                        toast: true,
                        position: "top-end",
                    });
                    return;
                }
                // Si non dans la wishlist, ajouter
                await axios.post(`http://localhost:8000/api/wishlist/`, {
                    user_id: userId,
                    book_id: bookId
                });
                setIsWishlisted(true); // Met à jour l'état immédiatement
                await Swal.fire({
                    icon: "success",
                    title: t("added_to_wishlist"),
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    toast: true,
                    position: "top-end",
                });
            }
        } catch (error) {
            console.error("Error handling wishlist:", error);
            await Swal.fire({
                icon: "error",
                title: t("error_wishlist"),
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
                toast: true,
                position: "top-end",
            });
        }
    };
    const handleReadToggle = async (bookId) => {
        try {
            if (isRead) {
                // Remove from read
                await axios.delete(`http://localhost:8000/api/user/${userId}/read/${bookId}`);
                setIsRead(false);
                await Swal.fire({
                    icon: "success",
                    title: t("removed_from_read"),
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    toast: true,
                    position: "top-end",
                });
            } else {
                // Cannot read if liked
                if (isLiked) {
                    await Swal.fire({
                        icon: "error",
                        title: t("cannot_read_liked_book"),
                        showConfirmButton: false,
                        timer: 3000,
                        timerProgressBar: true,
                        toast: true,
                        position: "top-end",
                    });
                    return;
                }
                // If wishlisted, remove from wishlist first
                if (isWishlisted) {
                    await axios.delete(`http://localhost:8000/api/user/${userId}/wishlist/${bookId}`);
                    setIsWishlisted(false);
                }
                // Add to read
                await axios.post(`http://localhost:8000/api/readbook/`, {
                    user_id: userId,
                    book_id: bookId
                });
                setIsRead(true);
                await Swal.fire({
                    icon: "success",
                    title: isWishlisted ? t("removed_from_wishlist_and_read") : t("added_to_read"),
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    toast: true,
                    position: "top-end",
                });
            }
        } catch (error) {
            console.error("Error handling read status:", error);
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

    const handleRating = async (rating) => {
        try {
            if (!userId) {
                await Swal.fire({
                    icon: "error",
                    title: t("must_be_logged_in"),
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    toast: true,
                    position: "top-end",
                });
                return;
            }

            await axios.post(`http://localhost:8000/api/books/${book_id}/rate`, {
                user_id: userId,
                rating: rating
            });

            setUserRating(rating);
            await Swal.fire({
                icon: "success",
                title: t("rating_saved"),
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
                toast: true,
                position: "top-end",
            });
        } catch (error) {
            console.error("Error saving rating:", error);
            const errorMessage = error.response?.status === 400 
                ? (error.response.data.message === "Un livre dans wishlist ne peut être noté" 
                    ? t("cannot_rate_wishlisted_book")
                    : error.response.data.message === "Un livre ni lu, ni liké ne peut être noté"
                        ? t("cannot_rate_unread_book")
                        : t("error_rating"))
                : t("error_rating");
                
            await Swal.fire({
                icon: "error",
                title: errorMessage,
                showConfirmButton: false,
                timer: 5000,
                timerProgressBar: true,
                toast: true,
                position: "top-end",
            });
        }
    };

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
                {book?.book_cover && book.book_cover !== "" ? (
                    <img
                        src={book.book_cover}
                        alt={book?.book_title || "Livre inconnu"}
                        onError={(e) => {
                            console.log("Image loading error");
                            e.target.style.display = 'none';
                            e.target.nextElementSibling.style.display = 'block';
                        }}
                    />
                ) : (
                    <ImageUnvailable width={"auto"} height={"auto"}/>
                )}
                    <div className="book-info">
                        <h1>{translatedTitle ? translatedTitle : t("unknown")}</h1>
                        <p className="author">
                            {t("book_author")}: {book.authors || t("unknown")}
                        </p>
                        <p>
                            <strong>{t("book_genres")}</strong>: {translatedGenres || t("no_genres")}
                        </p>
                        <p className={`description ${isDescriptionExpanded ? "expanded" : ""}`}>
                            <strong>{t("book_description")}</strong>: {translatedDesc ? translatedDesc : book.book_description || t("no_description")}
                        </p>
                        {translatedDesc && translatedDesc.length > 0 && translatedDesc.split(" ").length > 150 && (
                            <span className="see-more-button" onClick={toggleDescription}>
                                {isDescriptionExpanded ? t("book_see_less") : t("book_see_more")}
                            </span>
                        )}
                        <div style={{display: "flex", marginBottom: "10px", alignItems: "center"}}>
                            <strong>{t("book_avg_rating")}</strong>:
                            <StarIcon sx={{ 
                                color: "#FFD700",
                                marginLeft: "5px"
                            }}/> 
                            {book.book_avg_rating || t("not_rated")}
                        </div>

                        <div style={{display: "flex", alignItems: "center", marginBottom: "10px"}}>
                            <strong>{t("book_user_rating")}</strong>: 
                            <div 
                                style={{display: "flex", position: "relative", marginLeft: "5px"}}
                                onMouseLeave={() => setHoveredRating(0)}
                            >
                                {[...Array(5)].map((_, i) => (
                                    <div 
                                        key={i} 
                                        style={{position: "relative", cursor: "pointer"}}
                                        onClick={() => handleRating(hoveredRating || i + 1)}
                                        onMouseMove={(e) => {
                                            const rect = e.currentTarget.getBoundingClientRect();
                                            const halfPoint = (e.clientX - rect.left) < rect.width / 2;
                                            setHoveredRating(halfPoint ? i + 0.5 : i + 1);
                                        }}
                                    >
                                        {(() => {
                                            const rating = hoveredRating || userRating;
                                            if (i + 0.5 === rating) {
                                                return <StarHalfIcon sx={{ color: "#FFD700" }}/>;
                                            } else if (i + 1 <= rating) {
                                                return <StarIcon sx={{ color: "#FFD700" }}/>;
                                            }
                                            return <StarOutlineIcon sx={{ color: "#FFD700" }}/>;
                                        })()}
                                    </div>
                                ))}
                            </div>
                        </div>
                        {userId && (
                            <div className="action-buttons">
                                <div
                                    className="like-button"
                                    onClick={() => handleLikeToggle(book.book_id)}
                                    style={{color: isLiked ? "red" : "gray"}}
                                >
                                    {isLiked ? <FavoriteIcon fontSize="large"/> : <FavoriteBorderIcon fontSize="large"/>}
                                </div>
                                
                                <div
                                    className="wishlist-button"
                                    onClick={() => handleWishlistToggle(book.book_id)}
                                     style={{color: isWishlisted ? "#FFD700" : "gray"}}
                                >
                                    {isWishlisted ? <BookmarkIcon fontSize="large"/> : <BookmarkBorderIcon fontSize="large"/>}
                                </div>
                                <div
                                    className="read-button"
                                    onClick={() => handleReadToggle(book.book_id)}
                                    style={{color: isRead ? "#4CAF50" : "gray"}}
                                >
                                    {isRead ? <AutoStoriesIcon fontSize="large"/> : <AutoStoriesOutlinedIcon fontSize="large"/>}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </>
    );
}

export default BookDetails;
