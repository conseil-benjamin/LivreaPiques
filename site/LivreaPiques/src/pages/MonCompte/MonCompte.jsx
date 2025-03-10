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
    const navigate = useNavigate();
    const userId = Cookies.get('user_id');

    useEffect(() => {
        if (!userId) {
            setError('ID utilisateur non défini');
            setLoading(false);
            navigate('/');
        }
        const fetchUserProfile = async () => {
            try {
                const response = await fetch(`http://localhost:8000/api/user/${userId}/profile`);
                if (!response.ok) {
                    throw new Error('Erreur lors de la récupération des données');
                }
                const data = await response.json();
                setUserProfile(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchUserProfile();
    }, [userId]);

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
                {userProfile.liked_books.length > 0 ? (
                    <div style={{maxHeight: '300px', overflowY: 'scroll'}}>
                        <ul style={{listStyleType: 'none', padding: 0}}>
                            {userProfile.liked_books.map((book, index) => (
                                <li key={index} style={{marginBottom: '10px', display: 'flex', alignItems: 'center'}}>
                                    <div
                                        onClick={() => navigate(`/book/${book.book_id}`)}
                                        style={{display: 'flex', alignItems: 'center', cursor: 'pointer' }}
                                    >
                                        {book[0]?.book_cover && book[0].book_cover !== "null" && book[0].book_cover !== "" ? (
                                            <img
                                                src={book[0].book_cover}
                                                alt={book[0]?.book_title || "Livre inconnu"}
                                                style={{width: 'auto', height: '100px', borderRadius: '8px'}}
                                                onError={(e) => {
                                                    console.log("Image loading error");
                                                    e.target.style.display = 'none';
                                                    e.target.nextElementSibling.style.display = 'block';
                                                }}
                                            />
                                        ) : (
                                            <ImageUnvailable />
                                        )}
                                        <span>{book.book_description.length > 50 ? `${book.book_description.substring(0, 50)}...` : book.book_description}</span>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>
                ) : (
                    <p>{t("no_liked_books")}</p>
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
