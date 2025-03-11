import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import en from "./locales/en.json";
import fr from "./locales/fr.json";
import Cookies from "js-cookie";
import Swal from "sweetalert2";

// Initialisation de i18n avec la langue par défaut définie par les cookies ou "fr"
i18n
    .use(initReactI18next)
    .init({
        resources: {
            en: { translation: en },
            fr: { translation: fr },
        },
        lng: Cookies.get("lang") || "fr", // Si la langue n'est pas définie dans les cookies, on prend "fr"
        fallbackLng: "en",
        interpolation: {
            escapeValue: false,
        },
    });

// Écouter les changements de langue pour mettre à jour les cookies et afficher une notification
i18n.on("languageChanged", (lang) => {
    Cookies.set("lang", lang); // Stocker la langue sélectionnée dans les cookies
    Swal.fire({
        position: "top-end",
        icon: "success",
        title: `Langue changée avec succès vers ${lang}`,
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true,
        toast: true,
    });
});

export default i18n;
