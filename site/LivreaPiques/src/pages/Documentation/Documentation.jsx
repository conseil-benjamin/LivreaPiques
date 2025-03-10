import React from 'react';
import { useTranslation } from 'react-i18next';
import './Documentation.scss';
import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";

const Documentation = () => {
    const { t } = useTranslation();

    return (
        <>
            <Banner/>
            <div className="documentation-container">
                <h1 className="title">{t('documentation.title')}</h1>

                <div className="sections">
                    <section className="section">
                        <h2 className="section-title">{t('documentation.prerequisites.title')}</h2>
                        <p className="section-text">{t('documentation.prerequisites.description')}</p>
                        <ul className="list">
                            {t('documentation.prerequisites.list', { returnObjects: true }).map((item, index) => (
                                <li key={index}>{item}</li>
                            ))}
                        </ul>
                    </section>

                    <section className="section">
                        <h2 className="section-title">{t('documentation.installation.title')}</h2>

                        {[1, 2, 3].map(step => (
                            <div key={step} className="subsection">
                                <h3 className="subsection-title">{t(`documentation.installation.step${step}.title`)}</h3>
                                {t(`documentation.installation.step${step}.description`) && (
                                    <p className="section-text">{t(`documentation.installation.step${step}.description`)}</p>
                                )}
                                <div className="code-block">
                                    <pre>{t(`documentation.installation.step${step}.command`)}</pre>
                                </div>
                                {step === 2 && (
                                    <div className="install-info">
                                        <p className="section-text">{t('documentation.installation.step2.notInstalled.description')}</p>
                                        <ul className="list">
                                            {t('documentation.installation.step2.notInstalled.options', { returnObjects: true }).map((option, index) => (
                                                <li key={index}>{option}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                                {step === 3 && (
                                    <p className="note">{t('documentation.installation.step3.note')}</p>
                                )}
                            </div>
                        ))}
                    </section>

                    <section className="section">
                        <h2 className="section-title">{t('documentation.access.title')}</h2>
                        <p className="section-text">{t('documentation.access.description')}</p>
                        <ul className="list">
                            {t('documentation.access.options', { returnObjects: true }).map((option, index) => (
                                <li key={index}>{option}</li>
                            ))}
                        </ul>
                    </section>

                    <section className="section">
                        <h2 className="section-title">{t('documentation.commands.title')}</h2>
                        <div className="code-block">
                            <pre>{t('documentation.commands.list')}</pre>
                        </div>
                    </section>

                    <section className="section">
                        <h2 className="section-title">{t('documentation.troubleshooting.title')}</h2>
                        <ul className="list">
                            {t('documentation.troubleshooting.list', { returnObjects: true }).map((item, index) => (
                                <li key={index}>{item}</li>
                            ))}
                        </ul>
                    </section>
                </div>
            </div>
            <Footer/>
        </>
    );
};

export default Documentation;
