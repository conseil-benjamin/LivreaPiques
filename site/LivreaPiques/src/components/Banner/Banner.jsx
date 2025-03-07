import React, {useEffect, useState} from "react";
import "./Banner.scss";
import Swal from "sweetalert2";
import {useNavigate} from "react-router-dom";
import Cookies from "js-cookie";
import LanguageSwitcher from "../LanguageSwitcher/LanguageSwitcher.jsx";

function Banner() {
    const navigate = useNavigate();
    const jwt = Cookies.get("user_id");
    const [loginClicked, setLoginClicked] = useState(false);
    const [registerClicked, setRegisterClicked] = useState(false);

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
                {!jwt ? (
                        <div style={{display: "flex", alignItems: "center"}}>
                            <LoginComposant jwt={jwt} setLoginClicked={setLoginClicked} setRegisterClicked={setRegisterClicked}/>
                            <LanguageSwitcher/>
                        </div>
                    ): (
                    <div style={{display: "flex", alignItems: "center", justifyContent: "center"}}>
                        <Compte/>
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
                        Connexion
                    </button>
                    <button onClick={() => setRegisterClicked(true)}>
                        S'inscrire
                    </button>
                </>
            )}
        </div>
    )
}

function Compte() {
    const navigate = useNavigate();

    return (
        <div className={"compte"}>
            <button>
                <h1 style={{color: "#fff", cursor: "pointer"}} onClick={() => navigate("/profile")}>Mon compte</h1>
            </button>
        </div>
    )
}

export default Banner;
