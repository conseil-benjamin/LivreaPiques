export async function translateText(text, targetLang) {
    try {
        const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=en|${targetLang}`;
        const response = await fetch(url);
        const data = await response.json();

        if (data.responseData.translatedText) {
            return data.responseData.translatedText;
        } else {
            return text; // Si ça rate, on retourne la version originale
        }
    } catch (error) {
        console.error("Erreur de traduction :", error);
        return text;
    }
}
