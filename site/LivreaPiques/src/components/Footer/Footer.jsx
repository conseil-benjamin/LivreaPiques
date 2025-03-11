
import "./Footer.scss"
import HR from "../HR.jsx";
import {useNavigate} from "react-router-dom";
import Cookies from "js-cookie";
import {useTranslation} from "react-i18next";

function Footer() {
    const navigate = useNavigate();
    const userId = Cookies.get("user_id")
    const {t} = useTranslation();
    return (
        <footer className={"footer"}>
            <div style={{display: "flex", flexDirection: "row", alignItems: "center", margin: "0 0 1em 1em"}}>
                <img style={{borderRadius: "50px"}} src={"./bigboss.png"} alt={"logo"}  width={50}
                     height={50}/>
                <h1 style={{margin: "0 0 0 0.8em"}}>Big Book Society</h1>
            </div>
            <h5 style={{margin: "0 0 1em 1em"}}>{t("footer_title")}</h5>
            <h3>Navigation</h3>
            <div>
                <h5 onClick={() => navigate("/")}>Accueil</h5>
                <h5 onClick={() => navigate("/contact")}>Contact</h5>
                <h5 onClick={() => {userId ? navigate("/profile") : navigate("/login")}}>{t("footer_navigation_profile")}</h5>
                <h5 onClick={() => navigate("/documentation")}>{t("footer_navigation_documentation")}</h5>
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
