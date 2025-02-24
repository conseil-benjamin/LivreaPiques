import "./Login.scss"
import {useNavigate} from "react-router-dom";

function Login() {
    const navigate = useNavigate();
    return (
        <>
        <div className={"div-going-back"}>
            <img
                 style={{cursor: "pointer"}}
                 src={"https://cdn-icons-png.flaticon.com/512/3114/3114883.png"}
                 alt={"retour"}
                 width={30}
                 height={30}
                 onClick={() => {
                     navigate(-1)
                 }}
            />
        </div>
    <div className={"login"}>
        <form className={"form-login"}>
            <h1>Connexion</h1>
            <input type="text" placeholder={"Pseudo"}/>
                <input type="password" placeholder={"Mot de passe"}/>
                <button type="submit">Se connecter</button>
            </form>
        </div>
        </>
    )
}

export default Login