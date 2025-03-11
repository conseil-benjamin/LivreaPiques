import React, { useState } from 'react';
import './Contact.scss';
import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";
import { useTranslation } from 'react-i18next';

const Contact = () => {
    const { t } = useTranslation();
    // Données de l'équipe - remplacez avec vos vraies informations
    const teamMembers = [
            {
            id: 0,
                name: "Stéfan Beaulieu",
                role: t("team.manager"),
                bio: t("team.bio_stefan"),
                email: "stefan.beaulieu@etudiant.univ-rennes.fr",
                image: "./stephane.jpg"
        },
            {
                id: 1,
                name: "Diane Monéger",
                role: t("team.database_admin"),
            bio: t("team.bio_diane"),
            email: "diane.moneger@etudiant.univ-rennes.fr",
            image: "./diane.jpg"
        },
        {
            id: 2,
                name: "Ethan Brehin",
            role: t("team.fullstack_dev"),
            bio: t("team.bio_ethan"),
            email: "ethan.brehin@etudiant.univ-rennes.fr",
            image: "./ethan.jpg"
        },
        {
            id: 3,
                name: "Benjamin Conseil",
            role: t("team.fullstack_dev"),
            bio: t("team.bio_benjamin"),
            email: "benjamin.conseil@etudiant.univ-rennes.fr",
            image: "./benjamin.png"
        },
        {
            id: 4,
                name: "Esteban Debroise",
            role: t("team.data_ia"),
            bio: t("team.bio_esteban"),
            email: "esteban.debroise@etudiant.univ-rennes.fr",
            image: "./esteban.png"
        },
        {
            id: 5,
                name: "Pierig Malnoë",
            role: t("team.backend_dev"),
            bio: t("team.bio_pierig"),
            email: "pierig.malnoe@etudiant.univ-rennes.fr",
            image: "./pierig.png"
        },
        {
            id: 6,
                name: "Samuel Jouffe",
            role: t("team.system_admin"),
            bio: t("team.bio_samuel"),
            email: "samuel.jouffe@etudiant.univ-rennes.fr",
            image: "./samuel.png"
        }
    ];

    const [selectedMember, setSelectedMember] = useState(null);

    const handleMemberClick = (member) => {
        setSelectedMember(member);
    };

    const closeModal = () => {
        setSelectedMember(null);
    };

    return (
        <>
        <Banner />
        <div className="team-contact-page">
            {/* En-tête */}
            <div className="header">
                <h1>{t("team_title")}</h1>
                <p>
                    {t("team_description")}
                </p>
            </div>

            {/* Grille des membres de l'équipe */}
            <div className="team-grid">
                {teamMembers.map((member) => (
                    <div
                        key={member.id}
                        className="team-member-card"
                        onClick={() => handleMemberClick(member)}
                    >
                        <img
                            src={member.image}
                            alt={member.name}
                        />
                        <div className="member-info">
                            <h3>{member.name}</h3>
                            <p className="member-role">{member.role}</p>
                        </div>
                    </div>
                ))}
            </div>

            {/* Section Contact */}
            <div className="contact-section">
                <div className="contact-container">
                    <div className="contact-form">
                        <h2>{t("contact_us")}</h2>
                        <p>
                            {t("contact_description")}
                        </p>
                        <form>
                            <div className="form-group">
                                <label htmlFor="name">{t("form_name")}</label>
                                <input type="text" id="name" />
                            </div>
                            <div className="form-group">
                                <label htmlFor="email">{t("form_email")}</label>
                                <input type="email" id="email" />
                            </div>
                            <div className="form-group">
                                <label htmlFor="message">{t("form_message")}</label>
                                <textarea id="message" rows="4"></textarea>
                            </div>
                            <button type="submit">{t("form_send")}</button>
                        </form>
                    </div>
                    <div className="contact-info">
                        <h3>{t("info_title")}</h3>
                        <div className="info-items">
                            <p className="info-item">
                                <svg className="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                                <span>Rue Édouard Branly, 22300 Lannion, France</span>
                            </p>
                            <p className="info-item">
                                <svg className="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                </svg>
                                <span>contact@bigbooksociety.com</span>
                            </p>
                            <p className="info-item">
                                <svg className="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                                </svg>
                                <span>+33 1 23 45 67 89</span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Modal avec détails du membre */}
            {selectedMember && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <div className="modal-container">
                            <button
                                onClick={closeModal}
                                className="close-button"
                            >
                                <svg className="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                            <img
                                src={selectedMember.image}
                                alt={selectedMember.name}
                            />
                            <div className="modal-body">
                                <h3>{selectedMember.name}</h3>
                                <p className="member-role">{selectedMember.role}</p>
                                <p className="member-bio">{selectedMember.bio}</p>
                                <div className="member-email">
                                    <svg className="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                    </svg>
                                    <a href={`mailto:${selectedMember.email}`}>
                                        {selectedMember.email}
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
            <Footer/>
        </>
    );
};

export default Contact;