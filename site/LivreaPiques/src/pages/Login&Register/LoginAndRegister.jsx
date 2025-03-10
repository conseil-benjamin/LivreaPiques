import Cookies from "js-cookie";
import {useEffect, useState} from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./LoginAndRegister.scss"
import validator from "validator";
import Swal from "sweetalert2";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChevronUp, faChevronDown } from '@fortawesome/free-solid-svg-icons'
import {t} from "i18next";

function LoginAndRegister() {
    const navigate = useNavigate();
    const location = useLocation();
    const isLoginPage = location.pathname.includes("login");
    const [password, setPassword] = useState("");
    const [username, setUsername] = useState("");
    const [age, setAge] = useState("");
    const [gender, setGender] = useState("");
    const [firstStepInscriptionAccomplished, setFirstStepInscriptionAccomplished] = useState(false);
    const [secondStepInscriptionAccomplished, setSecondStepInscriptionAccomplished] = useState(false);
    const [nbBooksReadByYear, setNbBooksReadByYear] = useState("");
    const [nbBooksForPleasure, setNbBooksForPleasure] = useState("");
    const [nbBooksForWork, setNbBooksForWork] = useState("");
    const [initatedBy, setInitiatedBy] = useState("");
    const [readingTime, setReadingTime] = useState("");
    const [choiceMotivation, setChoiceMotivation] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    return (
        <div className={"connexion-main"}>
            <img src={"https://cdn-icons-png.flaticon.com/512/3114/3114883.png"} alt={"icon back"} width={30}
                 height={30} onClick={
                () => {
                    navigate("/")
                }
            }/>
            <div className="login-register-container">
        <div className="card">
            <div className="card-header">
                <h2>{isLoginPage ? t("connexion_title_login") : t("connexion_title_register")}</h2>
                <h3>
                    {isLoginPage
                        ? t("connexion_description") : t("register_description")}
                    </h3>
                </div>

                <div className="toggle-buttons">
                    <button
                        className={isLoginPage ? "active" : ""}
                        onClick={() => navigate("/login")}
                    >
                        {t("connexion_button_login")}
                    </button>
                    <button
                        className={!isLoginPage ? "active" : ""}
                        onClick={() => navigate("/register")}
                    >
                        {t("connexion_button_register")}
                    </button>
                </div>

                <div className="form-section">
                    {isLoginPage ? (
                        <LoginForm username={username} setUsername={setUsername} password={password} setPassword={setPassword} navigate={navigate}/>
                    ) : (
                        <RegisterForm username={username} setUsername={setUsername} password={password} setPassword={setPassword} age={age} setAge={setAge} gender={gender} setGender={setGender} firstStepInscriptionAccomplished={firstStepInscriptionAccomplished} setFirstStepInscriptionAccomplished={setFirstStepInscriptionAccomplished} choiceMotivation={choiceMotivation} setChoiceMotivation={setChoiceMotivation} initatedBy={initatedBy} setInitiatedBy={setInitiatedBy} nbBooksForPleasure={nbBooksForPleasure} nbBooksForWork={nbBooksForWork} setNbBooksForPleasure={setNbBooksForPleasure} setNbBooksForWork={setNbBooksForWork} nbBooksReadByYear={nbBooksReadByYear} setNbBooksReadByYear={setNbBooksReadByYear} readingTime={readingTime} setReadingTime={setReadingTime} secondStepInscriptionAccomplished={secondStepInscriptionAccomplished} setSecondStepInscriptionAccomplished={setSecondStepInscriptionAccomplished} navigate={navigate} setIsLoading={setIsLoading} isLoading={isLoading}/>
                    )}
                </div>

                <div className="footer-text">
                    {isLoginPage ? (
                        <p>
                            {t("no_account")} ?{" "}
                            <span onClick={() => navigate("/register")}>{t("connexion_register_redirection")}</span>
                        </p>
                    ) : (
                        <p>
                            {t("already_account")} ?{" "}
                            <span onClick={() => navigate("/login")}>{t("connexion_login_redirection")}</span>
                        </p>
                    )}
                </div>
            </div>
        </div>
        </div>
    );
}

function LoginForm({ username, setUsername, password, setPassword, navigate}) {
    return (
        <div className="form">
            <div className="form-group">
                <label>{t("connexion_label_username")}</label>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Votre nom d'utilisateur"
                    required
                />
            </div>
            <div className="form-group">
                <label>{t("connexion_label_password")}</label>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Mot de passe"
                    required
                />
            </div>
            <button onClick={() => login(username, password, navigate)}>{t("connexion_button_login")}</button>
        </div>
    );
}

function RegisterForm({ username, setUsername, password, setPassword, age, setAge, gender, setGender, firstStepInscriptionAccomplished, setFirstStepInscriptionAccomplished,  nbBooksReadByYear, setNbBooksReadByYear, nbBooksForPleasure, setNbBooksForPleasure, nbBooksForWork, setNbBooksForWork, initatedBy, setInitiatedBy, readingTime, setReadingTime, choiceMotivation, setChoiceMotivation, secondStepInscriptionAccomplished, setSecondStepInscriptionAccomplished, navigate, setIsLoading, isLoading}) {
    const initiationOptions = ["Choisir", "Famille", "Ami(e)", "École", "Autodidacte"];
    const readingTimeOptions = ["Choisir", "Matin", "Après-midi", "Soir", "Nuit"];
    const motivationOptions = ["Choisir", "Couverture", "Résumé", "Recommandation", "Auteur"];
    const nbBooksReadByYearOptions = ["Choisir", "Je ne lis plus", "Je ne lis jamais", "1 à 5", "6 à 10", "11 à 20", "Plus de 20", ]
    const nbBooksPleasureOptions = ["Choisir", "0", "1 à 5", "6 à 10", "11 à 20", "Plus de 20", ]
    const nbBooksWorkOptions = ["Choisir", "0", "1 à 5", "6 à 10", "11 à 20", "Plus de 20", ]

    const [isOpen, setIsOpen] = useState(false);

    const handleFocus = () => {
        setIsOpen(true);
    };

    const handleBlur = () => {
        setIsOpen(false);
    };

    return (
        <>
        {firstStepInscriptionAccomplished === true ? (
            <div className="form">
                <div className="form-group">
                    <label>{t("connexion_number_books_read_by_year")}</label>
                    <div className="select-container">
                        <select value={nbBooksReadByYear} onChange={(e) => setNbBooksReadByYear(e.target.value)} onBlur={handleBlur}
                                onFocus={handleFocus}>
                            {nbBooksReadByYearOptions.map((option, index) => (
                                <option key={index} value={option}>{option}</option>
                            ))}
                        </select>
                        <FontAwesomeIcon
                            icon={isOpen ? faChevronUp : faChevronDown}
                            id={"dropdown-icon"}
                        />
                    </div>
                </div>
                <div className="form-group">
                    <label>{t("connexion_book_read_for_pleasure")}</label>
                    <div className="select-container">
                        <select value={nbBooksForPleasure} onChange={(e) => setNbBooksForPleasure(e.target.value)}
                                onBlur={handleBlur}
                                onFocus={handleFocus}>
                            {nbBooksPleasureOptions.map((option, index) => (
                                <option key={index} value={option}>{option}</option>
                            ))}
                        </select>
                        <FontAwesomeIcon
                            icon={isOpen ? faChevronUp : faChevronDown}
                            id={"dropdown-icon"}
                        />
                    </div>
                </div>
                <div className="form-group">
                    <label>{t("connexion_book_read_for_work")}</label>
                    <div className="select-container">
                        <select value={nbBooksForWork} onChange={(e) => setNbBooksForWork(e.target.value)}
                                onBlur={handleBlur}
                                onFocus={handleFocus}>
                            {nbBooksWorkOptions.map((option, index) => (
                                <option key={index} value={option}>{option}</option>
                            ))}
                        </select>
                        <FontAwesomeIcon
                            icon={isOpen ? faChevronUp : faChevronDown}
                            id={"dropdown-icon"}
                        />
                    </div>
                </div>
                <div className="form-group">
                    <label>{t("connexion_initiated_by")}</label>
                    <div className="select-container">
                        <select value={initatedBy} onChange={(e) => setInitiatedBy(e.target.value)} onBlur={handleBlur}
                                onFocus={handleFocus}>
                            {initiationOptions.map((option, index) => (
                                <option key={index} value={option}>{option}</option>
                            ))}
                        </select>
                        <FontAwesomeIcon
                            icon={isOpen ? faChevronUp : faChevronDown}
                            id={"dropdown-icon"}
                        />
                    </div>
                </div>
                <div className="form-group">
                    <label>{t("connexion_best_time_for_reading")}</label>
                    <div className="select-container">
                        <select value={readingTime} onChange={(e) => setReadingTime(e.target.value)} onBlur={handleBlur}
                                onFocus={handleFocus}>
                            {readingTimeOptions.map((option, index) => (
                                <option key={index} value={option}>{option}</option>
                            ))}
                        </select>
                        <FontAwesomeIcon
                            icon={isOpen ? faChevronUp : faChevronDown}
                            id={"dropdown-icon"}
                        />
                    </div>
                </div>
                <div className="form-group">
                    <label>{t("connexion_motivations_choose_books")}</label>
                    <div className="select-container">
                        <select value={motivationOptions} onChange={(e) => setChoiceMotivation(e.target.value)} onBlur={handleBlur}
                                onFocus={handleFocus}>
                            {motivationOptions.map((option, index) => (
                                <option key={index} value={option}>{option}</option>
                            ))}
                        </select>
                        <FontAwesomeIcon
                            icon={isOpen ? faChevronUp : faChevronDown}
                            id={"dropdown-icon"}
                        />
                    </div>
                </div>
                <button onClick={() => {
                    checkEtape2Inscription(
                        username,
                        password,
                        age,
                        gender,
                        nbBooksReadByYear,
                        nbBooksForPleasure,
                        nbBooksForWork,
                        initatedBy,
                        readingTime,
                        choiceMotivation,
                        setSecondStepInscriptionAccomplished,
                        secondStepInscriptionAccomplished,
                        navigate
                    );
                }
                }
                >
                    {isLoading ? "Chargement..." : "Finaliser l'inscription"}
                </button>
            </div>
        ) : (
            <div className="form">
                <div className="form-group">
                    <label>{t("connexion_label_username")}</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Votre nom d'utilisateur"
                        required
                    />
                </div>
                <div className="form-group">
                    <label>{t("connexion_label_password")}</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Mot de passe"
                        required
                    />
                </div>
                <div className="form-group">
                    <label>{t("connexion_label_age")}</label>
                    <input
                        type="number"
                        value={age}
                        onChange={(e) => setAge(e.target.value)}
                        placeholder="Votre âge"
                        required
                    />
                </div>
                <div className="form-group">
                    <label>Genre</label>
                    <div className="gender-buttons">
                        <button
                            style={{backgroundColor: gender === "M" ? "#000000" : "#FFFFFF", color: gender !== "M" ? "#000000" : "#FFFFFF"}}
                            type="button"
                            className={gender === "M" ? "active" : ""}
                            onClick={() => setGender("M")}
                        >
                            {t("connexion_gender_male")}
                        </button>
                        <button
                            style={{backgroundColor: gender === "F" ? "#000000" : "#FFFFFF", color: gender !== "F" ? "#000000" : "#FFFFFF"}}
                            type="button"
                            className={gender === "F" ? "active" : ""}
                            onClick={() => setGender("F")}
                        >
                            {t("connexion_gender_female")}
                        </button>
                        <button
                            style={{backgroundColor: gender === "A" ? "#000000" : "#FFFFFF", color: gender !== "A" ? "#000000" : "#FFFFFF"}}
                            type="button"
                            className={gender === "A" ? "active" : ""}
                            onClick={() => setGender("A")}
                        >
                            {t("connexion_gender_other")}
                        </button>
                    </div>
                </div>
                {/* todo : ajouter isLoading au click */}
                <button onClick={() =>
                    verifyValidityFormRegister(
                        username,
                        password,
                        age,
                        gender,
                        setFirstStepInscriptionAccomplished
                    )
                }
                >{isLoading ? t("loading") : t("connexion_step2_button")}
                </button>
            </div>
        )}
        </>
    );
}

function login(username, password, navigate) {

    fetch("http://localhost:8000/api/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name: username,
            password: password,
        }),
    }).then(r => {
        if (r.status === 200) {
            r.json().then((data) => {
                Swal.fire({
                    timer: 2000,
                    text: t("connexion_swal_success"),
                    icon: "success",
                    position: "top-end",
                    toast: true,
                    timerProgressBar: true,
                    showConfirmButton: false
                }).then(r =>
                    Cookies.set("user_id", data.user_id).then(navigate("/"))
                );
            });
        } else {
            Swal.fire({
                text: t("connexion_swal_error"),
                timer: 3000,
                icon: "error",
                toast: true,
                position: "top-end",
                timerProgressBar: true,
                showConfirmButton: false
            }).then(r =>
                console.log(r)
            );
        }
    });
}

async function verifyValidityFormRegister(username, password, age, gender, setFirstStepInscriptionAccomplished, setIsloading) {
    let hasSameUsername = false;
    if (!validator.isStrongPassword(password)) {
        Swal.fire({
            text: t("connexion_password_contrainsts"),
            icon: "error",
            confirmButtonText: "Ok",
        }).then(r =>
            console.log(r)
        );
    }
    if (age > 115 || age < 13) {
        Swal.fire({
            text: t("connexion_age_contraints"),
            icon: "error",
            confirmButtonText: "Ok",
        }).then(r =>
            setFirstStepInscriptionAccomplished(false)
        );
    }

    const response = await fetch(`http://localhost:8000/api/check_username_availabitily/${username}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (response.status === 409) {
      await Swal.fire({
            text: t("connexion_swal_username_error_already_taken"),
            icon: "error",
            confirmButtonText: "Ok",
        }).then(r =>
            hasSameUsername = true
        );
    }

    if ((age < 110 || age > 13) && validator.isStrongPassword(password) && gender !== "" && !hasSameUsername) {
        console.log(hasSameUsername)
        setFirstStepInscriptionAccomplished(true);
    }
}

function createInscription(
    username,
    password,
    age,
    gender,
    nbBooksReadByYear,
    nbBooksForPleasure,
    nbBooksForWork,
    initatedBy,
    readingTime,
    choiceMotivation,
    setSecondStepInscriptionAccomplished,
    secondStepInscriptionAccomplished,
    navigate
) {

    fetch("http://localhost:8000/api/create_user/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name: username,
            password: password,
            age: age,
            gender: gender,
            nb_book_per_year: nbBooksReadByYear,
            nb_book_pleasure: nbBooksForPleasure,
            nb_book_work: nbBooksForWork,
            initiated_by: initatedBy,
            reading_time: readingTime,
            choice_motivation: choiceMotivation,
        }),
    }).then(r => {
        if (r.status === 200) {
            r.json().then((data) => {
                Swal.fire({
                    timer: 2500,
                    text: t("connexion_swal_register_success"),
                    icon: "success",
                    position: "top-end",
                    toast: true,
                    timerProgressBar: true,
                    showConfirmButton: false
                }).then(r =>
                    Cookies.set("user_id", data.user_id).then(navigate("/"))
                );
            });
        } else{
            Swal.fire({
                text: t("connexion_swal_register_error"),
                timer: 3000,
                icon: "error",
                toast: true,
                position: "top-end",
                timerProgressBar: true,
                showConfirmButton: false
            }).then(r =>
                console.log(r)
            );
        }
    });
}

    function checkEtape2Inscription(
        username,
        password,
        age,
        gender,
        nbBooksReadByYear,
        nbBooksForPleasure,
        nbBooksForWork,
        initatedBy,
        readingTime,
        choiceMotivation,
        setSecondStepInscriptionAccomplished,
        secondStepInscriptionAccomplished,
        navigate
    ) {
        // todo : vérifier si l'étape 2 de l'inscription est correcte
        if (nbBooksReadByYear === 0 || nbBooksForPleasure === 0 || nbBooksForWork === 0 || initatedBy === "" || readingTime === "" || choiceMotivation === "") {
            Swal.fire({
                text: "Veuillez remplir tous les champs",
                icon: "error",
                confirmButtonText: "Ok",
            }).then(r =>
                console.log(r)
            );
        } else {
            createInscription(
                username,
                password,
                age,
                gender,
                nbBooksReadByYear,
                nbBooksForPleasure,
                nbBooksForWork,
                initatedBy,
                readingTime,
                choiceMotivation,
                setSecondStepInscriptionAccomplished,
                secondStepInscriptionAccomplished,
                navigate
            )
        }
}

export default LoginAndRegister;
