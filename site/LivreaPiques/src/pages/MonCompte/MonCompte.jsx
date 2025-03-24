import React, { useEffect, useState } from 'react';
import './MonCompte.scss';
import {useNavigate} from "react-router-dom";
import Cookies from "js-cookie";
import Banner from "../../components/Banner/Banner.jsx";
import {t} from "i18next";
import ImageUnvailable from "../../components/ImageUnvailable.jsx";

function MonCompte() {
    const [userProfile, setUserProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [likedBooksDetails, setLikedBooksDetails] = useState([]); // Nouvel état
    const [wishlistBooksDetails, setWishlistBooksDetails] = useState([]); // Nouvel état    
    const [readBooksDetails, setReadBooksDetails] = useState([]); // nouvel état livre lu
    const navigate = useNavigate();
    const userId = Cookies.get('user_id');

    // Fonction pour récupérer les détails des livres
    const fetchBooksDetails = async (books, setStateFunction) => {
        try {
            const promises = books.map(book => 
                fetch(`http://localhost:8000/api/books/${book.book_id}`)
                    .then(res => res.json())
                    .then(data => Array.isArray(data) ? data[0] : data) // Extrait le premier élément si c'est un tableau
            );
            const booksData = await Promise.all(promises);
            setStateFunction(booksData);
        } catch (err) {
            console.error("Erreur lors de la récupération des détails des livres:", err);
        }
    };

    useEffect(() => {
        if (!userId) {
            setError('ID utilisateur non défini');
            setLoading(false);
            navigate('/');
        }
        const fetchUserProfile = async () => {
            try {
                // Get user profile data
                const response = await fetch(`http://localhost:8000/api/user/${userId}/profile`);
                if (!response.ok) {
                    throw new Error('Erreur lors de la récupération des données');
                }
                const data = await response.json();

                 // Récupère les livres de la liste de lecture
                try {
                    const wishlistResponse = await fetch(`http://localhost:8000/api/user/${userId}/wishlist`);
                    if (wishlistResponse.ok) {
                        const wishlistData = await wishlistResponse.json();
                        data.wishlist_books = wishlistData || []; // Si rien n'est dans la wishlist, on met un tableau vide (évite erreur)
                    } else {
                        data.wishlist_books = [];
                    }
                } catch (error) {
                    console.log("Erreur, aucun livre trouvé", error);
                    data.wishlist_books = [];
                }

                // Récupère les livres lus s'il y en a
                try {
                    const readBooksResponse = await fetch(`http://localhost:8000/api/user/${userId}/readbooks`);
                    if (readBooksResponse.ok) {
                        const readBooksData = await readBooksResponse.json();
                        data.read_books = readBooksData || []; //Pareil que pour la wishlist, évite l'erreur
                    } else {
                        data.read_books = [];
                    }
                } catch (error) {
                    console.log("Erreur, aucun livre trouvé", error);
                    data.read_books = [];
                }


                setUserProfile(data);
                // Récupérer les détails des livres aimés
                if (data.liked_books && data.liked_books.length > 0) {
                    await fetchBooksDetails(data.liked_books, setLikedBooksDetails);
                }
                // Récupérer les détails des livres de la wishlist
                if (data.wishlist_books && data.wishlist_books.length > 0) {
                    await fetchBooksDetails(data.wishlist_books, setWishlistBooksDetails);
                }
                // Récupérer les détails des livres lus
                if (data.read_books && data.read_books.length > 0) {
                    await fetchBooksDetails(data.read_books, setReadBooksDetails);
                }
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchUserProfile();
    }, [userId, navigate]);

    if (loading) {
        return <div style={{height: "100vh", display: "flex", alignItems: "center", justifyContent: "center"}}>
            {t("loading")}
        </div>;
    }

    if (error) {
        return <div>Erreur: {error}</div>;
    }

    const handleDeconnexion = () => {
        Cookies.remove('user_id');
        navigate('/');
    }

    const fetchBookDetails = async (bookId) => {
        try {
            // Get book data
            const response = await fetch(`http://localhost:8000/api/books/${bookId}`);
            if (!response.ok) {
                throw new Error('Erreur lors de la récupération des données');
            }
            const data = await response.json();

            return data;
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="profile-page">
            <Banner/>
            <div className="profile-info">
                <h2>{t("profile_title")}</h2>
                <p><strong>{t("username")}:</strong> {userProfile.username}</p>
                <p><strong>{t("age")}:</strong> {userProfile.age}</p>
                <p><strong>{t("gender")}:</strong> {userProfile.gender}</p>
                <p><strong>{t("books_per_year")}:</strong> {userProfile.nb_book_per_year}</p>
                <p><strong>{t("books_for_pleasure")}:</strong> {userProfile.nb_book_pleasure}</p>
                <p><strong>{t("books_for_work")}:</strong> {userProfile.nb_book_work}</p>
                <p><strong>{t("initial_motivation")}:</strong> {userProfile.initiated_by}</p>
                <p><strong>{t("daily_reading_time")}:</strong> {userProfile.reading_time}</p>
                <p><strong>{t("reading_motivation")}:</strong> {userProfile.choice_motivation}</p>
            </div>

            <div className="liked-books">
                <h3>{t("books_i_have_liked")}</h3>
                {likedBooksDetails.length > 0 ? (
                    <div style={{maxHeight: '300px', overflowY: 'scroll'}}>
                        <ul style={{listStyleType: 'none', padding: 0}}>
                            {likedBooksDetails.map((book, index) => (
                                <li key={index} style={{marginBottom: '10px', display: 'flex', alignItems: 'center'}}>
                                    {console.log(book)}
                                    <div
                                        onClick={() => navigate(`/book/${book.book_id}`)}
                                        style={{display: 'flex', alignItems: 'center', cursor: 'pointer', minWidth: '30%'}}
                                    >
                                        {book?.book_cover && book.book_cover !== "" ? (
                                                <img
                                                    src={book.book_cover}
                                                    alt={book?.book_title || t("unknown")}
                                                    style={{width: 'auto', height: '100px', borderRadius: '8px'}}
                                                    onError={(e) => {
                                                        console.log("Image loading error");
                                                        e.target.style.display = 'none';
                                                        e.target.nextElementSibling.style.display = 'block';
                                                    }}
                                                />
                                        ) : (
                                            <ImageUnvailable width={"80px"} height={"100px"}/>
                                        )}
                                        <div style={{display: "flex", flexDirection: "column", alignItems: "start"}}>
                                            <h4 style={{margin: "0 0 0 0.5em"}}>
                                                {book.book_title || t("unknown")}
                                            </h4>
                                            <span style={{margin: "0 0 0 0.5em"}}>
                                                {book.book_description ? 
                                                    (book.book_description.length > 50 ? 
                                                        `${book.book_description.substring(0, 50)}...` 
                                                        : book.book_description)
                                                    : t("no_description")}
                                            </span>
                                        </div>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>
                ) : (
                    <p>{t("no_liked_books")}</p>
                )}
            </div>
            <div className="wishlisted-books">
                <h3>{t("books_in_my_wishlist")}</h3>
                {wishlistBooksDetails.length > 0 ? (
                    <div style={{maxHeight: '300px', overflowY: 'scroll'}}>
                        <ul style={{listStyleType: 'none', padding: 0}}>
                            {wishlistBooksDetails.map((book, index) => (
                                <li key={index} style={{marginBottom: '10px', display: 'flex', alignItems: 'center'}}>
                                    <div
                                        onClick={() => navigate(`/book/${book.book_id}`)}
                                        style={{display: 'flex', alignItems: 'center', cursor: 'pointer', minWidth: '30%'}}
                                    >
                                        {book?.book_cover && book.book_cover !== "" ? (
                                                <img
                                                    src={book.book_cover}
                                                    alt={book?.book_title || t("unknown")}
                                                    style={{width: 'auto', height: '100px', borderRadius: '8px'}}
                                                    onError={(e) => {
                                                        console.log("Image loading error");
                                                        e.target.style.display = 'none';
                                                        e.target.nextElementSibling.style.display = 'block';
                                                    }}
                                                />
                                        ) : (
                                            <ImageUnvailable width={"80px"} height={"100px"}/>
                                        )}
                                        <div style={{display: "flex", flexDirection: "column", alignItems: "start"}}>
                                            <h4 style={{margin: "0 0 0 0.5em"}}>
                                                {book.book_title || t("unknown")}
                                            </h4>
                                            <span style={{margin: "0 0 0 0.5em"}}>
                                                {book.book_description ? 
                                                    (book.book_description.length > 50 ? 
                                                        `${book.book_description.substring(0, 50)}...` 
                                                        : book.book_description)
                                                    : t("no_description")}
                                            </span>
                                        </div>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>
                ) : (
                    <p>{t("no_wishlisted_books")}</p>
                )}
            </div>
            <div className="read-books">
                <h3>{t("books_i_have_read")}</h3>
                {readBooksDetails.length > 0 ? (
                    <div style={{maxHeight: '300px', overflowY: 'scroll'}}>
                        <ul style={{listStyleType: 'none', padding: 0}}>
                            {readBooksDetails.map((book, index) => (
                                <li key={index} style={{marginBottom: '10px', display: 'flex', alignItems: 'center'}}>
                                    <div
                                        onClick={() => navigate(`/book/${book.book_id}`)}
                                        style={{display: 'flex', alignItems: 'center', cursor: 'pointer', minWidth: '30%'}}
                                    >
                                        {book?.book_cover && book.book_cover !== "" ? (
                                                <img
                                                    src={book.book_cover}
                                                    alt={book?.book_title || t("unknown")}
                                                    style={{width: 'auto', height: '100px', borderRadius: '8px'}}
                                                    onError={(e) => {
                                                        console.log("Image loading error");
                                                        e.target.style.display = 'none';
                                                        e.target.nextElementSibling.style.display = 'block';
                                                    }}
                                                />
                                        ) : (
                                            <ImageUnvailable width={"80px"} height={"100px"}/>
                                        )}
                                        <div style={{display: "flex", flexDirection: "column", alignItems: "start"}}>
                                            <h4 style={{margin: "0 0 0 0.5em"}}>
                                                {book.book_title || t("unknown")}
                                            </h4>
                                            <span style={{margin: "0 0 0 0.5em"}}>
                                                {book.book_description ? 
                                                    (book.book_description.length > 50 ? 
                                                        `${book.book_description.substring(0, 50)}...` 
                                                        : book.book_description)
                                                    : t("no_description")}
                                            </span>
                                        </div>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>
                ) : (
                    <p>{t("no_read_books")}</p>
                )}
            </div>
            <div style={{width: "100%", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 0 2em 0"}}>
                <button style={{borderRadius: "10px", backgroundColor: "red", padding: "1em", color: "#fff", cursor: "pointer"}} onClick={() => handleDeconnexion()}>
                    <h4>{t("button_deconnexion")}</h4>
                </button>
            </div>
        </div>
    );
}

export default MonCompte;
