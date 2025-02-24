import {useNavigate} from "react-router-dom";
import Banner from "../../components/Banner/Banner";
import "./HomePage.scss";

function HomePage() {
    const navigate = useNavigate();

  return (
      <>
          <Banner />
        <div className={"home-page"}>
          <h1>Home Page</h1>
        </div>
      </>
  );
}

export default HomePage;