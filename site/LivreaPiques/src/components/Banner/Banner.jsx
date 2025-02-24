import "./Banner.scss";
import {useState} from "react";

function Banner() {
    const [searchValue, setSearchValue] = useState("");

    return (
        <div className={"banner"}>
            <img src={"https://cdn-icons-png.flaticon.com/512/54/54481.png"} alt="logo" />
            <div>
                <input
                    type="text"
                    value={searchValue}
                    placeholder="Search"
                    onChange={(e) => setSearchValue(e.target.value)}
                />
                <img src={"https://cdn-icons-png.flaticon.com/512/54/54481.png"} alt={"img serach"} />
            </div>
            <img src={"https://cdn-icons-png.flaticon.com/512/456/456212.png"} alt={"logo user"}/>
        </div>
    );
}

export default Banner;