import "./Footer.scss"
import HR from "../HR.jsx";
import {useNavigate} from "react-router-dom";
import Cookies from "js-cookie";
import {useTranslation} from "react-i18next";
import { useState, useEffect } from "react";

function Footer() {
    const navigate = useNavigate();
    const userId = Cookies.get("user_id")
    const {t} = useTranslation();
    const [isManager, setIsManager] = useState(false);

    useEffect(() => {
        const checkManagerStatus = async () => {
            if (userId) {
                try {
                    const response = await fetch(`http://localhost:8000/api/user/${userId}/is_manager`);
                    const data = await response.json();
                    setIsManager(data.is_manager);
                } catch (error) {
                    console.error("Erreur lors de la vérification du statut manager:", error);
                }
            }
        };
        checkManagerStatus();
    }, [userId]);

    return (
        <footer className={"footer"}>
            <div style={{display: "flex", flexDirection: "row", alignItems: "center", margin: "0 0 1em 1em"}}>
                <img style={{borderRadius: "50px"}} src={"./bigboss.png"} alt={"logo"}  width={50}
                     height={50}/>
                <h1 style={{margin: "0 0 0 0.8em"}}>Big Book Society</h1>
            </div>
            <h5 style={{margin: "0 0 1em 1em", cursor: "inherit"}}>{t("footer_title")}</h5>
            <h3>Navigation</h3>
            <div>
                <h5 onClick={() => navigate("/")}>Accueil</h5>
                <h5 onClick={() => navigate("/contact")}>Contact</h5>
                <h5 onClick={() => navigate("/documentation")}>{t("footer_navigation_documentation")}</h5>
                {isManager && <h5 onClick={() => navigate("/manage")}>{t("footer_navigation_manage")}</h5>}
                <h5 onClick={() => {userId ? navigate("/profile") : navigate("/login")}}>{t("footer_navigation_profile")}</h5>
            </div>
            {/*
            <h3>Légal</h3>
            <div>
                <h5 onClick={() => navigate("conditions-utilisations")}>Conditions d'utilisation</h5>
            </div>
            */}
            <h3>Contact</h3>
            <div>
                <h5>contact@bigbooksociety@gmail.com</h5>
            </div>
            <HR/>
            <p className={"footer-p"}>{t("footer_rights")}</p>
        </footer>
    );
}

export default Footer;
