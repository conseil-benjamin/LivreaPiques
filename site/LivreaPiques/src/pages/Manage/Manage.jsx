import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Manage.scss';
import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";
import { useTranslation } from 'react-i18next';
import Cookies from 'js-cookie';
import ImageUnvailable from "../../components/ImageUnvailable.jsx";

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
            setPredictionsMessage(t('manage.predictions.calculating'));
            const response = await fetch('http://localhost:8000/api/predictions/post_sales', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setPredictionsMessage(t('manage.predictions.success'));
                fetchPredictions(); // Fetch predictions after running them
            } else {
                setPredictionsMessage(t('manage.predictions.error'));
            }
        } catch (error) {
            console.error('Erreur:', error);
            setPredictionsMessage(t('manage.predictions.server_error'));
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

    const downloadPredictions = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/predictions/export');
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'sales_predictions.json';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error('Erreur lors du téléchargement:', error);
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
                            <button onClick={downloadPredictions}>{t("manage.stats.export")}</button>
                        </div>
                    </section>
                </div>
                
                {/* Liste unique des prédictions */}
                {predictions.length > 0 && (
                    <div className="predictions-section">
                        <h2>{t("manage_predictions_title")}</h2>
                        <div className="predictions-list">
                            <ul>
                                {predictions.map((prediction, index) => (
                                    <li key={index} className="prediction-item">
                                        {prediction.cover ? (
                                            <img 
                                                src={prediction.cover} 
                                                alt={prediction.title}
                                                className="book-cover"
                                            />
                                        ) : (
                                            <ImageUnvailable height={"150px"} width={"100px"}/>
                                        )}
                                        <div className="book-info">
                                            <h3>{prediction.title}</h3>
                                            <p className="authors">{prediction.authors}</p>
                                            <p className="genres">{prediction.genres}</p>
                                            <p className="score">Score: {(prediction.weight * 100).toFixed(0)}%</p>
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
