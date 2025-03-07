import React from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import "./Error404.scss";

function Page404() {
    const navigate = useNavigate();
    const { t } = useTranslation();

    return (
        <div className="page-404">
            <h1>404</h1>
            <h2>{t("error_404")}</h2>
            <button onClick={() => navigate("/")}>{t("go_back_404")}</button>
        </div>
    );
}

export default Page404;
