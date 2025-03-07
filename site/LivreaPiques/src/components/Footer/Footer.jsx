
import "./Footer.scss"
import HR from "../HR.jsx";
import {useNavigate} from "react-router-dom";

function Footer() {
    const navigate = useNavigate();
    return (
        <footer className={"footer"}>
            <div style={{display: "flex", flexDirection: "row", alignItems: "center", margin: "0 0 1em 1em"}}>
                <img style={{borderRadius: "50px"}} src={"./bigboss.png"} alt={"logo"}  width={50}
                     height={50}/>
                <h1 style={{margin: "0 0 0 0.8em"}}>LivreaPiques</h1>
            </div>
            <h5 style={{margin: "0 0 1em 1em"}}>Votre plateforme de recommandation de livres intelligente</h5>
            <h3>Navigation</h3>
            <div>
                <h5 onClick={() => navigate("/")}>Accueil</h5>
                <h5 onClick={() => navigate("/contact")}>Contact</h5>
                <h5 onClick={() => navigate("/login")}>Connexion</h5>
            </div>
            <h3>Légal</h3>
            <div>
                <h5 onClick={() => navigate("conditions-utilisations")}>Conditions d'utilisation</h5>
            </div>
            <h3>Contact</h3>
            <div>
                <h5>contact@livreApiques@gmail.com</h5>
            </div>
            <HR/>
            <p className={"footer-p"}>© 2025 LivreaPiques. Tous droits réservés.</p>
        </footer>
    );
}

export default Footer;
