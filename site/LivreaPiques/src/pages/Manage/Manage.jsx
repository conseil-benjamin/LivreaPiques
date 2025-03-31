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
    const [showAddBookForm, setShowAddBookForm] = useState(false);
    const [isPartOfSeries, setIsPartOfSeries] = useState(false);
    const [authorSuggestions, setAuthorSuggestions] = useState([]);
    const [awardSuggestions, setAwardSuggestions] = useState([]);
    const [seriesSuggestions, setSeriesSuggestions] = useState([]);
    const [formInputs, setFormInputs] = useState({
        author: "",
        awards: "",
        series_name: "",
        // ...other fields...
    });

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

    const handleAddBookClick = () => {
        setShowAddBookForm(!showAddBookForm);
    };

    const handleToggleSeries = () => {
        setIsPartOfSeries(!isPartOfSeries);
    };

    const fetchSuggestions = async (query, endpoint, setSuggestions) => {
        if (query.length > 0) {
            try {
                const response = await fetch(`http://localhost:8000/api/${endpoint}?q=${query}`);
                const data = await response.json();
                setSuggestions(data);
            } catch (error) {
                console.error(`Erreur lors de la récupération des suggestions pour ${endpoint}:`, error);
            }
        } else {
            setSuggestions([]);
        }
    };

    const handleAuthorInputChange = (e) => {
        fetchSuggestions(e.target.value, "authors", setAuthorSuggestions);
    };

    const handleAwardInputChange = (e) => {
        fetchSuggestions(e.target.value, "awards", setAwardSuggestions);
    };

    const handleSeriesInputChange = (e) => {
        fetchSuggestions(e.target.value, "series", setSeriesSuggestions);
    };

    const handleSuggestionClick = (value, setInputValue, fieldName) => {
        setInputValue((prevState) => ({
            ...prevState,
            [fieldName]: value,
        }));
        setAuthorSuggestions([]);
        setAwardSuggestions([]);
        setSeriesSuggestions([]);
    };

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
                            <button onClick={handleAddBookClick}>{t("manage.books.add_new")}</button>
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
                {showAddBookForm && (
                    <div className="add-book-form">
                        <h2>{t("manage.books.add_new")}</h2>
                        <form>
                            <label>
                                {t("Titre")}
                                <input type="text" name="title" />
                            </label>
                            <label>
                                {t("ISBN")}
                                <input type="text" name="isbn" />
                            </label>
                            <label>
                                {t("ISBN13")}
                                <input type="text" name="isbn13" />
                            </label>
                            <label>
                                {t("Auteur")}
                                <input
                                    type="text"
                                    name="author"
                                    value={formInputs.author}
                                    onChange={(e) =>
                                        setFormInputs({ ...formInputs, author: e.target.value })
                                    }
                                    onInput={handleAuthorInputChange}
                                />
                                {authorSuggestions.length > 0 && (
                                    <ul className="autocomplete-list">
                                        {authorSuggestions.map((author, index) => (
                                            <li
                                                key={index}
                                                onClick={() =>
                                                    handleSuggestionClick(
                                                        author.author_name,
                                                        setFormInputs,
                                                        "author"
                                                    )
                                                }
                                            >
                                                {author.author_name}
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </label>
                            <label>
                                {t("Récompenses")}
                                <input
                                    type="text"
                                    name="awards"
                                    value={formInputs.awards}
                                    onChange={(e) =>
                                        setFormInputs({ ...formInputs, awards: e.target.value })
                                    }
                                    onInput={handleAwardInputChange}
                                />
                                {awardSuggestions.length > 0 && (
                                    <ul className="autocomplete-list">
                                        {awardSuggestions.map((award, index) => (
                                            <li
                                                key={index}
                                                onClick={() =>
                                                    handleSuggestionClick(
                                                        award.award_name,
                                                        setFormInputs,
                                                        "awards"
                                                    )
                                                }
                                            >
                                                {award.award_name}
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </label>
                            <label>
                                {t("Couverture")}
                                <input type="file" name="cover" />
                            </label>
                            <label>
                                {t("Genres")}
                                <input type="text" name="genres" />
                            </label>
                            <label>
                                {t("Note moyenne")}
                                <input type="number" name="rating" min="0" max="5" step="0.1" />
                            </label>
                            <label>
                                {t("Editeur")}
                                <input type="text" name="publisher" />
                            </label>
                            <label>
                                {t("Fait partie d'une série")}
                                <input type="checkbox" onChange={handleToggleSeries} />
                            </label>
                            {isPartOfSeries && (
                                <label>
                                    {t("Nom de la série")}
                                    <input
                                        type="text"
                                        name="series_name"
                                        value={formInputs.series_name}
                                        onChange={(e) =>
                                            setFormInputs({
                                                ...formInputs,
                                                series_name: e.target.value,
                                            })
                                        }
                                        onInput={handleSeriesInputChange}
                                    />
                                    {seriesSuggestions.length > 0 && (
                                        <ul className="autocomplete-list">
                                            {seriesSuggestions.map((series, index) => (
                                                <li
                                                    key={index}
                                                    onClick={() =>
                                                        handleSuggestionClick(
                                                            series.series_name,
                                                            setFormInputs,
                                                            "series_name"
                                                        )
                                                    }
                                                >
                                                    {series.series_name}
                                                </li>
                                            ))}
                                        </ul>
                                    )}
                                </label>
                            )}
                            <button type="submit">{t("manage.books.fields.submit")}</button>
                        </form>
                    </div>
                )}
            </div>
            <Footer />
        </div>
    );
}

export default Manage;
