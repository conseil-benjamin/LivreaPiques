import React, {useEffect, useState} from "react";
import "./Banner.scss";
import {useNavigate} from "react-router-dom";
import Cookies from "js-cookie";
import LanguageSwitcher from "../LanguageSwitcher/LanguageSwitcher.jsx";
import { useTranslation } from "react-i18next";

function Banner() {
    const navigate = useNavigate();
    const jwt = Cookies.get("user_id");
    const [loginClicked, setLoginClicked] = useState(false);
    const [registerClicked, setRegisterClicked] = useState(false);
    const { t } = useTranslation();
    useEffect(() => {
        if (loginClicked) {
            navigate("/login");
        } else if (registerClicked) {
            navigate("/register");
        }
    }, [loginClicked, registerClicked]);

    return (
        <header className={"banner"}>
            <div className={"banner-row"}>
                <div style={{display: "flex", flexDirection: "row", alignItems: "center"}}>
                    <img
                        style={{cursor: "pointer"}}
                        width={50}
                        height={50}
                        src={"/public/bigboss.png"} alt="logo"
                        onClick={() => {
                            navigate("/")
                        }
                        }/>
                    <h2 style={{color: "#fff", fontSize: "1.5rem", fontWeight: "bold"}}>Big Book Society</h2>
                </div>

                <div style={{display: "flex", alignItems: "center", flexDirection: "row"}}>
                    <h3 style={{margin: "0 1em 0 0", fontSize: "1.3rem", color: "#fff", cursor: "pointer"}}
                        onClick={() => navigate("/")}>{t("footer_navigation_accueil")}</h3>
                    <h3 style={{margin: "0 1em 0 0", fontSize: "1.3rem", color: "#fff", cursor: "pointer"}}
                        onClick={() => navigate("/contact")}>{t("footer_navigation_contact")}</h3>
                    <h3 style={{margin: "0 1em 0 0", fontSize: "1.3rem", color: "#fff", cursor: "pointer"}}
                        onClick={() => navigate("/documentation")}>{t("footer_navigation_documentation")}</h3>
                    {jwt && <Compte/>}
                </div>

                {!jwt ? (
                    <div style={{display: "flex", alignItems: "center"}}>
                        <LoginComposant jwt={jwt} setLoginClicked={setLoginClicked}
                                        setRegisterClicked={setRegisterClicked}/>
                        <LanguageSwitcher/>
                        </div>
                    ): (
                    <div style={{display: "flex", alignItems: "center", justifyContent: "center"}}>
                        <LanguageSwitcher/>
                    </div>
                )}
            </div>
            <hr style={{
                height: "1px",
                width: "100%"
            }}/>
        </header>
    );
}

function LoginComposant({ jwt, setLoginClicked, setRegisterClicked }) {
    const {t} = useTranslation();
    return (
        <div className={"login-composant"}>
            {jwt ? (
                <img
                    style={{cursor: "pointer"}}
                    src={"https://cdn-icons-png.flaticon.com/512/456/456212.png"}
                    alt={"logo user"}
                    width={40}
                    height={40}
                    onClick={() => {
                        navigate("/login")
                    }}
                />
            ) : (
                <>
                    <button onClick={() => setLoginClicked(true)}>
                        {t("banner_login")}
                    </button>
                    <button onClick={() => setRegisterClicked(true)}>
                        {t("banner_register")}
                    </button>
                </>
            )}
        </div>
    )
}

function Compte() {
    const navigate = useNavigate();
    const {t} = useTranslation();

    return (
        <div className={"compte"}>
            <button>
                <h3 style={{margin: "0 1em 0 0", fontSize: "1.3rem", color: "#fff", cursor: "pointer"}} onClick={() => navigate("/profile")}>{t("banner_my_profile")}</h3>
            </button>
        </div>
    )
}

export default Banner;
