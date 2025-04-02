import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Manage.scss';
import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";
import { useTranslation } from 'react-i18next';
import Cookies from 'js-cookie';
import UploadFileIcon from '@mui/icons-material/UploadFile'; // Import Material-UI upload icon

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
    const [genreSuggestions, setGenreSuggestions] = useState([]);
    const [publisherSuggestions, setPublisherSuggestions] = useState([]); // State for publisher suggestions
    const [selectedGenres, setSelectedGenres] = useState([]);
    const [selectedAwards, setSelectedAwards] = useState([]);
    const [formInputs, setFormInputs] = useState({
        author: "",
        awards: "",
        series_name: "",
        publisher: "",
        title: "",
        isbn: "",
        isbn13: "",
        rating: "0",
        genres: "",
        cover: null, // Ensure this is null for file inputs
    });
    const [isAuthorUnknown, setIsAuthorUnknown] = useState(false);
    const [isDragging, setIsDragging] = useState(false);
    const [previewImage, setPreviewImage] = useState(null); // State to store the preview image

    const handleAuthorUnknownToggle = () => {
        setIsAuthorUnknown(!isAuthorUnknown);
        if (!isAuthorUnknown) {
            setFormInputs((prevState) => ({ ...prevState, author: "Inconnu" }));
        } else {
            setFormInputs((prevState) => ({ ...prevState, author: "" }));
        }
    };

    const handleGenreInputChange = (e) => {
        fetchSuggestions(e.target.value, "genres", setGenreSuggestions);
    };

    const handleGenreSelect = (genre) => {
        if (!selectedGenres.includes(genre)) {
            setSelectedGenres([...selectedGenres, genre]);
        }
        setGenreSuggestions([]);
    };

    const handleGenreRemove = (genre) => {
        setSelectedGenres(selectedGenres.filter((g) => g !== genre));
    };

    const handleAwardInputChange = (e) => {
        fetchSuggestions(e.target.value, "awards", setAwardSuggestions);
    };

    const handleAwardSelect = (award) => {
        if (!selectedAwards.includes(award)) {
            setSelectedAwards([...selectedAwards, award]);
        }
        setAwardSuggestions([]);
    };

    const handleAwardRemove = (award) => {
        setSelectedAwards(selectedAwards.filter((a) => a !== award));
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith("image/")) {
            setPreviewImage(URL.createObjectURL(file)); // Set the preview image
        } else {
            alert("Veuillez déposer uniquement des fichiers image.");
        }
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file && file.type.startsWith("image/")) {
            setPreviewImage(URL.createObjectURL(file)); // Set the preview image
        } else {
            alert("Veuillez sélectionner uniquement des fichiers image.");
        }
    };

    const handleRemoveImage = () => {
        setPreviewImage(null); // Remove the preview image
    };

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
                if (endpoint === "genres" && Array.isArray(data)) {
                    setSuggestions(data.map((item) => item.genre_name)); // Map to genre_name
                } else if (endpoint === "awards" && Array.isArray(data)) {
                    setSuggestions(data); // Awards are already a flat list
                } else if (endpoint === "authors" && Array.isArray(data)) {
                    setSuggestions(data); // Authors are already a flat list
                } else if (endpoint === "publishers" && Array.isArray(data)) {
                    setSuggestions(data); // Publishers are already a flat list
                } else if (endpoint === "series" && Array.isArray(data)) {
                    setSuggestions(data.map((item) => item.series_name)); // Map to series_name
                } else {
                    setSuggestions([]); // Ensure suggestions are cleared if data is invalid
                    console.error(`Unexpected response format for ${endpoint}:`, data);
                }
            } catch (error) {
                console.error(`Erreur lors de la récupération des suggestions pour ${endpoint}:`, error);
            }
        } else {
            setSuggestions([]); 
        }
    };

    const handleAuthorInputChange = (e) => {
        const value = e.target.value || ""; 
        setFormInputs((prevState) => ({ ...prevState, author: value }));
        fetchSuggestions(value, "authors", setAuthorSuggestions);
    };

    const handlePublisherInputChange = (e) => {
        const value = e.target.value || ""; 
        setFormInputs((prevState) => ({ ...prevState, publisher: value }));
        fetchSuggestions(value, "publishers", setPublisherSuggestions); 
    };

    const handleSeriesInputChange = (e) => {
        const value = e.target.value || ""; // chaine de caractères
        setFormInputs((prevState) => ({ ...prevState, series_name: value }));
        fetchSuggestions(value, "series", setSeriesSuggestions); // chercher les suggestions
    };

    const handleSuggestionClick = (value, setInputValue, fieldName) => {
        setInputValue((prevState) => ({
            ...prevState,
            [fieldName]: value,
        }));
        setAuthorSuggestions([]);
        setAwardSuggestions([]);
        setSeriesSuggestions([]);
        setPublisherSuggestions([]);
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
                                <input
                                    type="text"
                                    name="title"
                                    value={formInputs.title || ""} // Ensure controlled input
                                    onChange={(e) =>
                                        setFormInputs((prevState) => ({
                                            ...prevState,
                                            title: e.target.value,
                                        }))
                                    }
                                />
                            </label>
                            <label>
                                {t("ISBN")}
                                <input
                                    type="text"
                                    name="isbn"
                                    value={formInputs.isbn || ""} // Ensure controlled input
                                    onChange={(e) =>
                                        setFormInputs((prevState) => ({
                                            ...prevState,
                                            isbn: e.target.value,
                                        }))
                                    }
                                />
                            </label>
                            <label>
                                {t("ISBN13")}
                                <input
                                    type="text"
                                    name="isbn13"
                                    value={formInputs.isbn13 || ""} // Ensure controlled input
                                    onChange={(e) =>
                                        setFormInputs((prevState) => ({
                                            ...prevState,
                                            isbn13: e.target.value,
                                        }))
                                    }
                                />
                            </label>
                            <label className="author-field">
                                {t("Auteur")}
                                <div className="author-input-container">
                                    <input
                                        type="text"
                                        name="author"
                                        value={formInputs.author || ""} // Ensure controlled input
                                        onChange={handleAuthorInputChange}
                                        disabled={isAuthorUnknown}
                                    />
                                    <div className="author-unknown-checkbox">
                                        <input
                                            type="checkbox"
                                            checked={isAuthorUnknown}
                                            onChange={handleAuthorUnknownToggle}
                                        />
                                        <span>{t("Inconnu")}</span>
                                    </div>
                                </div>
                                {authorSuggestions.length > 0 && !isAuthorUnknown && (
                                    <ul className="autocomplete-list">
                                        {authorSuggestions.map((author, index) => (
                                            <li
                                                key={index}
                                                onClick={() =>
                                                    handleSuggestionClick(author, setFormInputs, "author")
                                                }
                                            >
                                                {author}
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
                                    onInput={handleAwardInputChange}
                                />
                                {awardSuggestions.length > 0 && (
                                    <ul className="autocomplete-list">
                                        {awardSuggestions.map((award, index) => (
                                            <li
                                                key={index}
                                                onClick={() => handleAwardSelect(award)}
                                            >
                                                {award}
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </label>
                            <div className="selected-awards">
                                {selectedAwards.map((award, index) => (
                                    <span key={index} className="award-tag">
                                        {award}
                                        <button
                                            type="button"
                                            onClick={() => handleAwardRemove(award)}
                                        >
                                            &times;
                                        </button>
                                    </span>
                                ))}
                            </div>
                            <label>
                                {t("Couverture")}
                                <div
                                    className={`file-drop-zone ${isDragging ? "dragging" : ""}`}
                                    onDragOver={handleDragOver}
                                    onDragLeave={handleDragLeave}
                                    onDrop={handleDrop}
                                >
                                    {previewImage ? (
                                        <div className="image-preview">
                                            <img src={previewImage} alt="Preview" />
                                            <button type="button" onClick={handleRemoveImage}>
                                                {t("Supprimer l'image")}
                                            </button>
                                        </div>
                                    ) : (
                                        <>
                                            <UploadFileIcon className="upload-icon" />
                                            <span>{t("Glissez et déposez un fichier ou cliquez pour télécharger")}</span>
                                            <input
                                                type="file"
                                                name="cover"
                                                accept="image/*"
                                                onChange={(e) => {
                                                    const file = e.target.files[0];
                                                    setFormInputs((prevState) => ({
                                                        ...prevState,
                                                        cover: file || null, // Ensure controlled input
                                                    }));
                                                    if (file && file.type.startsWith("image/")) {
                                                        setPreviewImage(URL.createObjectURL(file));
                                                    }
                                                }}
                                            />
                                        </>
                                    )}
                                </div>
                            </label>
                            <label>
                                {t("Genres")}
                                <input
                                    type="text"
                                    name="genres"
                                    value={formInputs.genres || ""} // Ensure controlled input
                                    onChange={(e) =>
                                        setFormInputs((prevState) => ({
                                            ...prevState,
                                            genres: e.target.value,
                                        }))
                                    }
                                    onInput={handleGenreInputChange}
                                />
                                {genreSuggestions.length > 0 && (
                                    <ul className="autocomplete-list">
                                        {genreSuggestions.map((genre, index) => (
                                            <li
                                                key={index}
                                                onClick={() => handleGenreSelect(genre)}
                                            >
                                                {genre}
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </label>
                            <div className="selected-genres">
                                {selectedGenres.map((genre, index) => (
                                    <span key={index} className="genre-tag">
                                        {genre}
                                        <button
                                            type="button"
                                            onClick={() => handleGenreRemove(genre)}
                                        >
                                            &times;
                                        </button>
                                    </span>
                                ))}
                            </div>
                            <label>
                                {t("Note moyenne")}
                                <input
                                    type="number"
                                    name="rating"
                                    value={formInputs.rating || "0"} // Ensure controlled input
                                    min="0"
                                    max="5"
                                    step="0.01"
                                    onChange={(e) =>
                                        setFormInputs((prevState) => ({
                                            ...prevState,
                                            rating: e.target.value,
                                        }))
                                    }
                                    onInput={(e) => {
                                        const value = parseFloat(e.target.value);
                                        if (value < 0) e.target.value = "0";
                                        if (value > 5) e.target.value = "5";
                                        if (!/^\d*(\.\d{0,2})?$/.test(e.target.value)) {
                                            e.target.value = value.toFixed(2);
                                        }
                                    }}
                                />
                            </label>
                            <label className="publisher-field">
                                {t("Editeur")}
                                <div className="publisher-input-container">
                                    <input
                                        type="text"
                                        name="publisher"
                                        value={formInputs.publisher || ""} // Ensure controlled input
                                        onChange={handlePublisherInputChange}
                                    />
                                </div>
                                {publisherSuggestions.length > 0 && (
                                    <ul className="autocomplete-list">
                                        {publisherSuggestions.map((publisher, index) => (
                                            <li
                                                key={index}
                                                onClick={() =>
                                                    handleSuggestionClick(publisher, setFormInputs, "publisher")
                                                }
                                            >
                                                {publisher}
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </label>
                            <label className="series-field">
                                {t("Fait partie d'une série")}
                                <input type="checkbox" onChange={handleToggleSeries} />
                            </label>
                            {isPartOfSeries && (
                                <label>
                                    {t("Nom de la série")}
                                    <input
                                        type="text"
                                        name="series_name"
                                        value={formInputs.series_name ?? ""} 
                                        onChange={(e) =>
                                            setFormInputs((prevState) => ({
                                                ...prevState,
                                                series_name: e.target.value,
                                            }))
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
                            <button type="submit">{t("Ajouter")}</button>
                        </form>
                    </div>
                )}
            </div>
            <Footer />
        </div>
    );
}

export default Manage;
