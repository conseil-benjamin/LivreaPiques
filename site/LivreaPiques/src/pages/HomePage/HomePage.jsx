import {useNavigate} from "react-router-dom";
import Banner from "../../components/Banner/Banner";
import "./HomePage.scss";
import Footer from "../../components/Footer/Footer.jsx";
import {useEffect, useState} from "react";
import { ChevronRight } from "lucide-react";
import axios from "axios";
import Cookies from "js-cookie";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import Slider from "react-slick";
import {useTranslation} from "react-i18next"; // Import de react-slick
import ImageUnvailable from "../../components/ImageUnvailable.jsx";

function HomePage() {
    const [searchValue, setSearchValue] = useState("");
    const userId = Cookies.get("user_id");
    const {t} = useTranslation();
    return (
        <div className={"home-page"}>
            <Banner/>
            {!userId && (
                <HeaderHomePage/>
            )}
            <SearchBar searchValue={searchValue} setSearchValue={setSearchValue}/>
            {!userId ? (
                <div className="home-page-explanation">
                    <h1>{t("why_choose_platform")}</h1>
                    <h2>{t("best_experience")}</h2>
                    <CardExplanation
                        title={t("feature_personal_library")}
                        description={t("desc_personal_library")}
                        img={"./book-bookmark.png"}
                    />
                    <CardExplanation
                        title={t("feature_ai_recommendations")}
                        description={t("desc_ai_recommendations")}
                        img={"./star.png"}
                    />
                    {/*
                    <CardExplanation
                        title={t("feature_active_community")}
                        description={t("desc_active_community")}
                        img={"./users.png"}
                    />
                    */}
                </div>
            ) : (
                <Recommandations/>
            )}
            <Footer/>
        </div>
    );
}


function Recommandations() {
    const [recoBooks, setRecoBooks] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const userId = Cookies.get("user_id");
    const navigate = useNavigate();
    const {t} = useTranslation();

    // Fonction pour récupérer les recommandations de livres
    const fetchRecommendations = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await axios.post("http://localhost:8000/api/reco2/", {id: userId});

            const bookIds = response.data.recommendations;

            if (bookIds && bookIds.length > 0) {
                const bookDetailsPromises = bookIds.map((bookId) =>
                    axios.get(`http://localhost:8000/api/books/${bookId}`)
                );

                const bookDetailsResponse = await Promise.all(bookDetailsPromises);

                const books = bookDetailsResponse.map((res) => res.data);

                // Sauvegarder les recommandations dans le localStorage
                localStorage.setItem('recoBooks', JSON.stringify(books));

                setRecoBooks(books);
            } else {
                setError("Aucune recommandation trouvée.");
            }
        } catch (err) {
            console.error("Erreur lors de la récupération des recommandations:", err);
            setError("Erreur lors de la récupération des recommandations.");
        } finally {
            setLoading(false);
        }
    };

    // Charger les recommandations depuis le localStorage lors du montage du composant
    useEffect(() => {
        const savedRecoBooks = localStorage.getItem('recoBooks');
        if (savedRecoBooks) {
            setRecoBooks(JSON.parse(savedRecoBooks));
        }
    }, []);

    // Configuration du carrousel
    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 3,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                }
            }
        ]
    };

    return (
        <div className="home-page-recommandations">
            <h1 style={{textAlign: "center", fontSize: "1.75rem"}}>{t("recommendations_title")}</h1>

            <div style={{display: "flex", alignItems: "center", justifyContent: "center", margin: "1em 0 1em 0"}}>
                <button style={{backgroundColor: "#000", color: "#fff", borderRadius: "10px", padding: "1em", cursor: "pointer"}} onClick={fetchRecommendations}>
                    <h3>{t("get_recommendations")}</h3>
                </button>
            </div>

            {loading && <p style={{textAlign: "center"}}>{t("recommandations_loading")}</p>}
            {error && <p style={{color: 'red'}}>{error}</p>}

            <div className="recommandations-list">
                {recoBooks.length > 0 && !loading && (
                    <Slider {...settings}>
                        {recoBooks.map((book, index) => (
                            <div key={index} className="book-card"
                                 onClick={() => navigate(`/book/${book[0].book_id}`)}>
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
                                <div>
                                    <h4>{book[0]?.book_title || "Titre inconnu"}</h4>
                                    <p>{book[0]?.book_description?.slice(0, 150)}...</p>
                                    <p>Auteur(s): {book[0]?.authors || 'Inconnu'}</p>
                                </div>
                            </div>
                        ))}
                    </Slider>
                )}
            </div>
        </div>
    );
}

function HeaderHomePage() {
    const navigate = useNavigate();
    const {t} = useTranslation();

    return (
        <header className={"home-page-header"}>
            <div>
                <div>
                    <div>
                        <h1>
                            {t("home_page_label")}
                        </h1>
                        <h4>
                            {t("home_page_description")}
                        </h4>
                        <div style={{display: "flex", flexDirection: "row", margin: "1em 0 0 0"}}>
                            <button style={{display: "flex", flexDirection: "row"}} onClick={() =>  navigate("/register")}>
                                {t("home_page_register")}
                                <ChevronRight size={18}/>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    )
}

function SearchBar() {
    const [searchValue, setSearchValue] = useState(""); // Valeur de recherche
    const [books, setBooks] = useState([]); // Pour stocker les résultats de la recherche
    const [debounceTimeout, setDebounceTimeout] = useState(null); // Pour stocker l'ID du setTimeout
    const [isLoading, setIsLoading] = useState(false); // Pour afficher un spinner de chargement
    const navigate = useNavigate();
    const {t} = useTranslation();

    // Fonction pour gérer la recherche
    const handleSearch = async () => {
        if (searchValue.length > 2) {  // Rechercher après 3 caractères
            try {
                // Appel à l'API pour récupérer les livres correspondants
                const response = await axios.get(`http://localhost:8000/api/books/search?query=${searchValue}`);
                setIsLoading(false)
                setBooks(response.data); // Mettre à jour les résultats
            } catch (error) {
                console.error("Erreur lors de la recherche:", error);
                setBooks([]); // Si erreur, réinitialiser les livres
            }
        } else {
            setBooks([]); // Si la recherche est vide ou trop courte, réinitialiser les livres
        }
    };

    // Fonction d'événement pour mettre à jour la valeur de recherche
    const handleChange = (e) => {
        const value = e.target.value;
        setSearchValue(value); // Mettre à jour la valeur de recherche

        // Si un délai existe, on le supprime pour en créer un nouveau
        if (debounceTimeout) {
            clearTimeout(debounceTimeout);
        }

        // Créer un nouveau délai de 1 seconde (1000 ms)
        const timeout = setTimeout(() => {
            setIsLoading(true); // Afficher le spinner de chargement
            handleSearch(); // Appeler la fonction de recherche après 1 seconde
        }, 1000);
        setDebounceTimeout(timeout); // Sauvegarder l'ID du setTimeout pour pouvoir le nettoyer si nécessaire
    };

    return (
        <div className="home-page-search-bar-main">
            <div className="home-page-search-bar">
                <input
                    type="text"
                    value={searchValue}
                    placeholder={t("placeholder_search")}
                    onChange={handleChange}
                />
                {isLoading ? (
                    <img
                        src="./menu-dots.png"
                        alt="spinner"
                        width={24}
                        height={24}
                    />
                ): (
                    <img
                        src="https://cdn-icons-png.flaticon.com/512/54/54481.png"
                        alt="img search"
                        width={24}
                        height={24}
                        style={{cursor: "pointer"}}
                    />
                )}

            </div>

            {/* Afficher les résultats de la recherche */}
            {books.length > 0 ? (
                <div className="search-results-list" style={{overflowY: 'scroll', maxHeight: '500px', marginTop: '20px' }}>
                    {books.map((book) => (
                        <div key={book.book_id} className="card" style={{
                            display: 'flex',
                            border: '1px solid #ddd',
                            borderRadius: '8px',
                            marginBottom: '20px',
                            padding: '10px',
                            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                            width: '100%',
                            flexDirection: 'row',
                            cursor: 'pointer'
                        }} onClick={() => navigate(`/book/${book.book_id}`)}>
                            <img
                                src={book.book_cover || "default-cover.jpg"} // Si pas de cover, mettre une image par défaut
                                alt={book.book_title}
                                style={{ width: '100px', height: 'auto', borderRadius: '8px' }}
                            />
                            <div style={{ marginTop: '10px' }}>
                                <h4 style={{ fontSize: '16px', fontWeight: 'bold' }}>{book.book_title}</h4>
                                <p style={{ fontSize: '14px', color: '#666' }}>
                                    {book.book_description.length > 150
                                        ? book.book_description.slice(0, 150) + '...' // Troncature de la description
                                        : book.book_description}
                                </p>
                                <p style={{ fontSize: '14px', color: '#888' }}>Auteur(s): {book.authors || 'Inconnu'}</p>
                            </div>
                        </div>
                    ))}
                </div>
            ) : searchValue !== "" && books.length === 0 ? (
                <div className="search-results-list">
                    <p style={{ textAlign: 'center' }}>{t("none_books_found")}</p>
                </div>
            ): null}
        </div>
    );
}

function CardExplanation(
    {title, description, img}
){
    return (
        <div className={"explanation-card"}>
            <div className={"explanation-card-div-img"}>
                <img src={img} alt={"img explanation"} width={40} height={40}/>
            </div>
            <div className={"explanation-card-div-content"}>
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
        </div>
    )
}

export default HomePage;