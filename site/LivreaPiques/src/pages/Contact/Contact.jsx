import React, { useState } from 'react';
import './Contact.scss';
import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";

const Contact = () => {
    // Données de l'équipe - remplacez avec vos vraies informations
    const teamMembers = [
        {
            id: 0,
            name: "Stéfan Beaulieu",
            role: "Manager",
            bio: "Stéfan est responsable de la gestion de l'équipe et de la stratégie globale de la plateforme. Son objectif est de s'assurer que tout fonctionne harmonieusement et que les utilisateurs aient une expérience fluide.",
            email: "stefan.beaulieu@etudiant.univ-rennes.fr",
            image: "./stephane.jpg"
        },
        {
            id: 1,
            name: "Diane Monéger",
            role: "Administratrice Base de données",
            bio: "Diane gère l'architecture et la gestion des bases de données, garantissant une organisation optimale des informations pour un accès rapide et sécurisé aux données des livres et des utilisateurs.",
            email: "diane.moneger@etudiant.univ-rennes.fr",
            image: "./diane.jpg"
        },
        {
            id: 2,
            name: "Ethan Brehin",
            role: "Développeur Full-Stack",
            bio: "Ethan est en charge du développement front-end et back-end de la plateforme, en s'assurant que les fonctionnalités de l'application soient performantes et adaptées aux besoins des utilisateurs.",
            email: "ethan.brehin@etudiant.univ-rennes.fr",
            image: "./ethan.jpg"
        },
        {
            id: 3,
            name: "Benjamin Conseil",
            role: "Développeur Full-Stack",
            bio: "Benjamin travaille sur l'ensemble du développement technique de la plateforme, en optimisant les fonctionnalités existantes et en ajoutant de nouvelles fonctionnalités pour améliorer l'expérience utilisateur.",
            email: "benjamin.conseil@etudiant.univ-rennes.fr",
            image: "./benjamin.png"
        },
        {
            id: 4,
            name: "Esteban Debroise",
            role: "Data IA",
            bio: "Esteban utilise des techniques d'intelligence artificielle et d'analyse de données pour personnaliser les recommandations de livres et améliorer l'algorithme de suggestion en fonction des préférences des utilisateurs.",
            email: "esteban.debroise@etudiant.univ-rennes.fr",
            image: "./esteban.png"
        },
        {
            id: 5,
            name: "Pierig Malnoë",
            role: "Développeur Back-End",
            bio: "Pierig est responsable de la gestion du côté serveur de la plateforme, en optimisant la performance et la sécurité des données tout en s'assurant que la base fonctionne de manière fiable et rapide.",
            email: "pierig.malnoe@etudiant.univ-rennes.fr",
            image: "./pierig.png"
        },
        {
            id: 6,
            name: "Samuel Jouffe",
            role: "Administrateur Système",
            bio: "Samuel s'occupe de l'administration et de la gestion des systèmes informatiques, en garantissant la stabilité, la sécurité et la performance des serveurs de la plateforme.",
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
                <h1>Notre Équipe</h1>
                <p>
                    Découvrez les passionnés de littérature qui ont créé cette plateforme de recommandations de livres pour vous aider à trouver votre prochaine lecture préférée.
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
                        <h2>Contactez-nous</h2>
                        <p>
                            Vous avez des questions ou des suggestions ? N'hésitez pas à nous contacter !
                        </p>
                        <form>
                            <div className="form-group">
                                <label htmlFor="name">Nom</label>
                                <input type="text" id="name" />
                            </div>
                            <div className="form-group">
                                <label htmlFor="email">Email</label>
                                <input type="email" id="email" />
                            </div>
                            <div className="form-group">
                                <label htmlFor="message">Message</label>
                                <textarea id="message" rows="4"></textarea>
                            </div>
                            <button type="submit">Envoyer</button>
                        </form>
                    </div>
                    <div className="contact-info">
                        <h3>Informations</h3>
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
                                <span>contact@livresapiques.com</span>
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