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
                        <h2>{t("manage.users.title")}</h2>
                        <div className="section-content">
                            <button>{t("manage.users.view_all")}</button>
                            <button>{t("manage.users.add_new")}</button>
                        </div>
                    </section>

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
                            <button>{t("manage.stats.view")}</button>
                            <button>{t("manage.stats.export")}</button>
                        </div>
                    </section>
                </div>
            </div>
            <Footer />
        </div>
    );
}

export default Manage;
