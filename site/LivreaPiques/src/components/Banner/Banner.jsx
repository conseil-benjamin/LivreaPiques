import "./Banner.scss";
import {useState} from "react";
import Swal from "sweetalert2";
import {useNavigate} from "react-router-dom";

function Banner() {
    const [searchValue, setSearchValue] = useState("");
    const navigate = useNavigate();

    return (
        <header className={"banner"}>
            <div className={"banner-row"}>
                <img
                    style={{cursor: "pointer"}}
                    width={50}
                    height={50}
                    src={"./bigboss.png"} alt="logo"
                    onClick={() => {
                        navigate("/")
                    }
                    }/>
                <div className={"div-input-search"}>
                    <input
                        type="text"
                        value={searchValue}
                        placeholder="Rechercher un livre"
                        onChange={(e) => setSearchValue(e.target.value)}
                    />
                    <img
                        src={"https://cdn-icons-png.flaticon.com/512/54/54481.png"}
                        alt={"img serach"}
                        width={24}
                        height={24}
                        style={{cursor: "pointer"}}
                    />
                </div>
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
            </div>

            <hr style={{
                height: "1px",
                width: "100%"
            }}/>
        </header>
    );
}

export default Banner;