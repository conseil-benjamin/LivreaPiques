import {useNavigate} from "react-router-dom";
import Banner from "../../components/Banner/Banner";
import "./HomePage.scss";
import Footer from "../../components/Banner/Footer/Footer.jsx";

function HomePage() {
    const navigate = useNavigate();

  return (
      <>
          <Banner />
        <div className={"home-page"}>
          <h1>Home Page</h1>
        </div>
          <Footer/>
      </>
  );
}

export default HomePage;