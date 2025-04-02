import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Manage.scss';
import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";
import { useTranslation } from 'react-i18next';
import Cookies from 'js-cookie';

function Manage() {
    const navigate = useNavigate();
    const { t } = useTranslation();
    const userId = Cookies.get('user_id');
    const [isManager, setIsManager] = useState(false);
    const [loading, setLoading] = useState(true);
    const [predictionsMessage, setPredictionsMessage] = useState('');
    const [predictions, setPredictions] = useState([]);

    useEffect(() => {
        // Vérifie si l'utilisateur est un manager
        const checkManagerStatus = async () => {
            try {
                const response = await fetch(`http://localhost:8000/api/user/${userId}/is_manager`);
                const data = await response.json();
                setIsManager(data.is_manager);
            } catch (error) {
                console.error("Erreur lors de la vérification du statut manager:", error);
                navigate('/');
            } finally {
                setLoading(false);
            }
        };

        if (!userId) {
            navigate('/');
        } else {
            checkManagerStatus();
        }
    }, [userId, navigate]);

    const runSalesPredictions = async () => {
        try {
            setPredictionsMessage('Calcul des prédictions en cours...');
            const response = await fetch('http://localhost:8000/api/predictions/post_sales', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setPredictionsMessage('Prédictions calculées avec succès!');
                fetchPredictions(); // Fetch predictions after running them
            } else {
                setPredictionsMessage('Erreur lors du calcul des prédictions.');
            }
        } catch (error) {
            console.error('Erreur:', error);
            setPredictionsMessage('Erreur lors de la communication avec le serveur.');
        }
    };

    const fetchPredictions = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/predictions/get_sales');
            if (response.ok) {
                const data = await response.json();
                setPredictions(data.predictions); // Les prédictions sont déjà triées côté serveur
            } else {
                console.error('Erreur lors de la récupération des prédictions.');
            }
        } catch (error) {
            console.error('Erreur:', error);
        }
    };

    useEffect(() => {
        fetchPredictions(); // Fetch predictions on component mount
    }, []);

    if (loading) {
        return <div>{t("loading")}</div>;
    }

    if (!isManager) {
        navigate('/');
        return null;
    }

    return (
        <div className="manage-page">
            <Banner />
            <div className="manage-container">
                <h1>{t("manage.title")}</h1>
                <div className="manage-sections">
                    <section className="manage-section">
                        <h2>{t("manage.books.title")}</h2>
                        <div className="section-content">
                            <button>{t("manage.books.view_all")}</button>
                            <button>{t("manage.books.add_new")}</button>
                        </div>
                    </section>

                    <section className="manage-section">
                        <h2>{t("manage.stats.title")}</h2>
                        <div className="section-content">
                            <button onClick={runSalesPredictions}>
                                {t("manage.stats.view")}
                            </button>
                            {predictionsMessage && (
                                <p className="predictions-message">{predictionsMessage}</p>
                            )}
                            <button>{t("manage.stats.export")}</button>
                        </div>
                    </section>
                </div>
                
                {/* Liste unique des prédictions */}
                {predictions.length > 0 && (
                    <div className="predictions-section">
                        <h2>{t("manage.predictions.title")}</h2>
                        <div className="predictions-list">
                            <ul>
                                {predictions.map((prediction, index) => (
                                    <li key={index} className="prediction-item">
                                        <img 
                                            src={prediction.cover} 
                                            alt={prediction.title}
                                            className="book-cover"
                                        />
                                        <div className="book-info">
                                            <h3>{prediction.title}</h3>
                                            <p className="authors">{prediction.authors}</p>
                                            <p className="genres">{prediction.genres}</p>
                                            <p className="score">Score: {prediction.weight}</p>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                )}
            </div>
            <Footer />
        </div>
    );
}

export default Manage;
