// todo :récupérer l'url de la page et en fonction de l'url affic

import Register from "./Register/Register.jsx";
import Login from "./Login/Login.jsx";

function LoginAndRegister() {
    const url = window.location.href;

  return (
    <div>
        {url.includes("login") ? <Login /> : <Register />}
    </div>
  );
}

export default LoginAndRegister;