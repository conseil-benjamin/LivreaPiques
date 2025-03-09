import {BrowserRouter as Router, Route, Routes, useLocation} from "react-router-dom";
import HomePage from "./pages/HomePage/HomePage.jsx";
import "./App.scss";
import LoginAndRegister from "./pages/Login&Register/LoginAndRegister.jsx";
import Contact from "./pages/Contact/Contact.jsx"
import BookDetails from "./pages/Book/BookDetails.jsx";
import ConditionsUtilisations from "./pages/ConditionsUtilisations/ConditionsUtilisations.jsx";
import Error404 from "./pages/Error404/Error404.jsx";
import MonCompte from "./pages/MonCompte/MonCompte.jsx";

function App() {

  return (
    <div>
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/about" element={<HomePage />} />
                <Route path="/login" element={<LoginAndRegister />} />
                <Route path="/register" element={<LoginAndRegister />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/book/:book_id" element={<BookDetails />} />
                <Route path="/conditions-utilisations" element={<ConditionsUtilisations />} />
                <Route path="/profile" element={<MonCompte />} />
                <Route path="*" element={<Error404 />} />
            </Routes>
        </Router>
    </div>
  )
}

export default App
