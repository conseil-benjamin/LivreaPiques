import React, { useEffect, useState } from 'react';
import './MonCompte.scss';
import {useNavigate} from "react-router-dom";
import Cookies from "js-cookie";

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
        return <div>Chargement...</div>;
    }

    if (error) {
        return <div>Erreur: {error}</div>;
    }

    return (
        <div className="profile-page">
            <div className="profile-info">
                <h2>Mon Profil</h2>
                <p><strong>Nom d'utilisateur:</strong> {userProfile.username}</p>
                <p><strong>Âge:</strong> {userProfile.age}</p>
                <p><strong>Genre:</strong> {userProfile.gender}</p>
                <p><strong>Livres par an:</strong> {userProfile.nb_book_per_year}</p>
                <p><strong>Livres de plaisir par an:</strong> {userProfile.nb_book_pleasure}</p>
                <p><strong>Livres de travail par an:</strong> {userProfile.nb_book_work}</p>
                <p><strong>Initialement motivé par:</strong> {userProfile.initiated_by}</p>
                <p><strong>Temps de lecture quotidien:</strong> {userProfile.reading_time}</p>
                <p><strong>Motivation pour la lecture:</strong> {userProfile.choice_motivation}</p>
            </div>

            <div className="liked-books">
                <h3>Livres que j'ai likés</h3>
                {userProfile.liked_books.length > 0 ? (
                    <ul>
                        {userProfile.liked_books.map((book, index) => (
                            <li key={index}>
                                <div onClick={() => navigate(`/book/${book.book_id}`)}>
                                    <img src={book.book_cover} alt={`Cover unknow`} style={{ width: '50px', height: '75px' }} />
                                    <p>{book.book_description}</p>
                                </div>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>Aucun livre liké pour l'instant.</p>
                )}
            </div>
            <div>
                <button>
                    <h4>Déconnexion</h4>
                </button>
            </div>
        </div>
    );
}

export default MonCompte;
