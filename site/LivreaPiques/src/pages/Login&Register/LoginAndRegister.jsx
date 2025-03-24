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
    const [isManagerAccount, setIsManagerAccount] = useState(false);

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
                {!isLoginPage && (
                    <div className="account-type-switch">
                        <label className="switch">
                            <input
                                type="checkbox"
                                checked={isManagerAccount}
                                onChange={() => setIsManagerAccount(!isManagerAccount)}
                            />
                            <span className="slider round"></span>
                        </label>
                        <span className="account-type-label">
                            {isManagerAccount ? t("manager_account") : t("user_account")}
                        </span>
                    </div>
                )}
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
                        <RegisterForm username={username} setUsername={setUsername} password={password} setPassword={setPassword} age={age} setAge={setAge} gender={gender} setGender={setGender} firstStepInscriptionAccomplished={firstStepInscriptionAccomplished} setFirstStepInscriptionAccomplished={setFirstStepInscriptionAccomplished} choiceMotivation={choiceMotivation} setChoiceMotivation={setChoiceMotivation} initatedBy={initatedBy} setInitiatedBy={setInitiatedBy} nbBooksForPleasure={nbBooksForPleasure} nbBooksForWork={nbBooksForWork} setNbBooksForPleasure={setNbBooksForPleasure} setNbBooksForWork={setNbBooksForWork} nbBooksReadByYear={nbBooksReadByYear} setNbBooksReadByYear={setNbBooksReadByYear} readingTime={readingTime} setReadingTime={setReadingTime} secondStepInscriptionAccomplished={secondStepInscriptionAccomplished} setSecondStepInscriptionAccomplished={setSecondStepInscriptionAccomplished} navigate={navigate} setIsLoading={setIsLoading} isLoading={isLoading} isManagerAccount={isManagerAccount}/>
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

function RegisterForm({ 
    username, 
    setUsername, 
    password, 
    setPassword, 
    age, 
    setAge, 
    gender, 
    setGender, 
    firstStepInscriptionAccomplished, 
    setFirstStepInscriptionAccomplished,
    nbBooksReadByYear,
    setNbBooksReadByYear,
    nbBooksForPleasure,
    setNbBooksForPleasure,
    nbBooksForWork,
    setNbBooksForWork,
    initatedBy,
    setInitiatedBy,
    readingTime,
    setReadingTime,
    choiceMotivation,
    setChoiceMotivation,
    secondStepInscriptionAccomplished,
    setSecondStepInscriptionAccomplished,
    navigate,
    setIsLoading,
    isLoading,
    isManagerAccount
}) {
    const [token, setToken] = useState("");

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

    const handleManagerRegistration = async () => {
        if (!username || !password || !token) {
            Swal.fire({
                text: t("connexion_fill_all_fields"),
                icon: "error",
                confirmButtonText: "Ok",
            });
            return;
        }

        // Ajout de la vérification du format du mot de passe
        if (!validator.isStrongPassword(password)) {
            Swal.fire({
                text: t("connexion_password_contrainsts"),
                icon: "error",
                confirmButtonText: "Ok",
            });
            return;
        }

        setIsLoading(true);
        try {
            const response = await fetch("http://localhost:8000/api/create_manager/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name: username,
                    password: password,
                    token: token,
                }),
            });

            if (response.status === 200) {
                const data = await response.json();
                await Swal.fire({
                    timer: 2500,
                    text: t("connexion_swal_register_success"),
                    icon: "success",
                    position: "top-end",
                    toast: true,
                    timerProgressBar: true,
                    showConfirmButton: false
                });
                Cookies.set("user_id", data.user_id);
                navigate("/");
            } else if (response.status === 409) {
                Swal.fire({
                    text: t("connexion_swal_username_error_already_taken"),
                    icon: "error",
                    confirmButtonText: "Ok",
                });
            } else if (response.status === 401) {
                Swal.fire({
                    text: t("connexion_invalid_token"),
                    icon: "error",
                    confirmButtonText: "Ok",
                });
            } else {
                const errorData = await response.json();
                Swal.fire({
                    text: errorData.detail || t("connexion_swal_register_error"),
                    icon: "error",
                    confirmButtonText: "Ok",
                });
            }
        } catch (error) {
            Swal.fire({
                text: t("connexion_swal_register_error"),
                icon: "error",
                confirmButtonText: "Ok",
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
        {!isManagerAccount && firstStepInscriptionAccomplished ? (
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
                        <select value={choiceMotivation} onChange={(e) => setChoiceMotivation(e.target.value)} onBlur={handleBlur}
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
                        navigate,
                        setIsLoading
                    );
                }
                }
                >
                    {isLoading ? t("loading") : t("connexion_finalise_inscription")}
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
                        placeholder={t("connexion_placeholder_username")}
                        required
                    />
                </div>
                <div className="form-group">
                    <label>{t("connexion_label_password")}</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder={t("connexion_placeholder_password")}
                        required
                    />
                </div>
                {isManagerAccount ? (
                    <div className="form-group">
                        <label>{t("connexion_label_token")}</label>
                        <input
                            type="text"
                            value={token}
                            onChange={(e) => setToken(e.target.value)}
                            placeholder={t("connexion_placeholder_token")}
                            required
                        />
                    </div>
                ) : (
                    <>
                        <div className="form-group">
                            <label>{t("connexion_label_age")}</label>
                            <input
                                type="number"
                                value={age}
                                onChange={(e) => setAge(e.target.value)}
                                placeholder={t("connexion_placeholder_age")}
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
                    </>
                )}
                <button 
                    onClick={isManagerAccount ? handleManagerRegistration : () =>
                        verifyValidityFormRegister(
                            username,
                            password,
                            age,
                            gender,
                            setFirstStepInscriptionAccomplished
                        )
                    }
                >
                    {isLoading ? t("loading") : (isManagerAccount ? t("connexion_finalise_inscription") : t("connexion_step2_button"))}
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
        return;
    }
    if (age < 13 || age > 115) {  // Correction de la condition
        Swal.fire({
            text: t("connexion_age_contraints"),
            icon: "error",
            confirmButtonText: "Ok",
        }).then(r =>
            setFirstStepInscriptionAccomplished(false)
        );
        return;
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
        return;
    }

    if (validator.isStrongPassword(password) && gender !== "" && !hasSameUsername) {  // Simplifié la condition
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
        navigate,
        setIsLoading
    ) {
        setIsLoading(true);
        if (nbBooksReadByYear === "Choisir" || 
            nbBooksForPleasure === "Choisir" || 
            nbBooksForWork === "Choisir" || 
            initatedBy === "Choisir" || 
            readingTime === "Choisir" || 
            choiceMotivation === "Choisir") {
            Swal.fire({
                text: t("connexion_fill_all_fields"),
                icon: "error",
                confirmButtonText: "Ok",
            });
            setIsLoading(false);
            return;
        }

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
        ).finally(() => {
            setIsLoading(false);
        });
    }

export default LoginAndRegister;
