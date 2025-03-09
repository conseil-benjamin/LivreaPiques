import { useTranslation } from "react-i18next";

function LanguageSwitcher() {
    const { i18n } = useTranslation();
    const lang = i18n.language;

    const changeLanguage = (lang) => {
        i18n.changeLanguage(lang);
    };

    return (
        <div>
            <button style={{cursor: "pointer", margin: "0.5em", backgroundColor: lang === "fr" && "#fff", borderRadius: "5px", padding: "0.5em"}} onClick={() => changeLanguage("fr")}>🇫🇷</button>
            <button style={{cursor: "pointer", margin: "0.5em", backgroundColor: lang === "en" && "#fff", borderRadius: "5px", padding: "0.5em"}} onClick={() => changeLanguage("en")}>🇬🇧</button>
        </div>
    );
}

export default LanguageSwitcher;
