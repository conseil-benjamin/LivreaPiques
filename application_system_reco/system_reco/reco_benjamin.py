import pandas as pd
import numpy as np
from supabase import create_client 
from sklearn.preprocessing import MinMaxScaler
from collections import Counter
from SQL_controleur.SQL_controleur import *

class FinalRecommender:
    def __init__(self):
        """
        Initialise le système de recommandation avec les données de Supabase.
        - Charge les tables liked_books, books et users
        - Calcule les scores de popularité des livres 
        - Prépare la structure pour la diversité des genres
        - Maintient un historique des recommandations
        """
        url = "https://pczyoeavtwijgtkzgcaz.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBjenlvZWF2dHdpamd0a3pnY2F6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzEzOTc1NTUsImV4cCI6MjA0Njk3MzU1NX0._KJBbSHWivEF6VrPdyO3TUI729c0eXnj-zoVeQmFYQc"
        self.supabase = create_client(url, key)

        # Chargement des données 
        #self.liked_books = pd.DataFrame(self.supabase.table("liked_books").select("*").order("book_id", desc=False).execute().data)
        self.liked_books = requete("SELECT * FROM liked_books ORDER BY book_id")
        #self.books = pd.DataFrame(self.supabase.table("book").select("*").order("book_id", desc=False).execute().data)
        self.books = requete("SELECT * FROM book ORDER BY book_id")
        #self.users = pd.DataFrame(self.supabase.table("user").select("*").execute().data)
        self.users = requete('''SELECT * FROM "user"''')
        
        # Historique des recommandations par utilisateur
        self.recommendation_history = {}
        
        # Affichage des statistiques du dataset
        print(f"Nombre total de livres : {len(self.books)}")
        print(f"Nombre total d'utilisateurs : {len(self.users)}")
        print(f"Nombre total de likes : {len(self.liked_books)}")
        
        # Calcul des métriques dérivées
        self.book_popularity = self._calculate_book_popularity()
        self.user_reading_patterns = self._calculate_user_reading_patterns()
        self.book_diversity_score = self._calculate_book_diversity_scores()

    def _calculate_book_popularity(self):
        """
        Calcule un score de popularité plus nuancé pour chaque livre.
        - Utilise une normalisation logarithmique pour réduire l'impact des best-sellers
        """
        popularity = self.liked_books['book_id'].value_counts()
        max_likes = popularity.max()
        normalized_popularity = popularity.apply(lambda x: np.log1p(x) / np.log1p(max_likes))
        return normalized_popularity

    def _calculate_user_reading_patterns(self):
        """
        Analyse les patterns de lecture pour identifier la diversité des goûts
        """
        user_patterns = {}
        for user_id in self.users['user_id'].unique():
            user_likes = self.liked_books[self.liked_books['user_id'] == user_id]
            if not user_likes.empty:
                liked_books = self.books[self.books['book_id'].isin(user_likes['book_id'])]
                user_patterns[user_id] = {
                    'total_likes': len(user_likes),
                    'unique_genres': len(liked_books['genre'].unique()) if 'genre' in self.books.columns else 0
                }
        return user_patterns

    def _calculate_book_diversity_scores(self):
        """
        Calcule un score de diversité par rapport aux livres populaires
        """
        diversity_scores = {}
        popular_books = self.book_popularity.nlargest(10).index
        
        for book_id in self.books['book_id']:
            if 'genre' in self.books.columns:
                book_genre = self.books[self.books['book_id'] == book_id]['genre'].iloc[0]
                popular_genres = self.books[self.books['book_id'].isin(popular_books)]['genre']
                genre_diversity = 1 - (sum(g == book_genre for g in popular_genres) / len(popular_genres))
                diversity_scores[book_id] = genre_diversity
            else:
                diversity_scores[book_id] = 0.5
        return diversity_scores

    def _convert_book_range(self, range_str):
        """
        Convertit les plages textuelles en valeurs numériques
        """
        if isinstance(range_str, (int, float)):
            return float(range_str)
        
        range_mapping = {
            '0': 0,
            'Je ne lis plus': 0,
            'Je ne lis jamais': 0,
            '1 à 5': 3,
            '5 à 10': 7.5,
            '10 à 15': 12.5,
            '15 à 20': 17.5,
            'Plus de 20': 25
        }
        return float(range_mapping.get(range_str, 0))

    def _create_user_profile_vector(self, user_id):
        """
        Crée un profil utilisateur enrichi avec patterns de lecture
        """
        try:
            user_matches = self.users[self.users['user_id'] == user_id]
            if user_matches.empty:
                return None
                
            user_info = user_matches.iloc[0]
            books_per_year = self._convert_book_range(user_info['nb_book_per_year'])
            scaler = MinMaxScaler()
            age_normalized = scaler.fit_transform([[float(user_info['age'])]])[0][0]
            books_per_year_normalized = scaler.fit_transform([[books_per_year]])[0][0]
            
            liked_books = self.liked_books[self.liked_books['user_id'] == user_id]
            reading_patterns = self.user_reading_patterns.get(user_id, {})
            
            return {
                'demographic': {
                    'age': age_normalized,
                    'gender': 1 if user_info['gender'] == 'M' else 0,
                    'books_per_year': books_per_year_normalized,
                    'raw_age': float(user_info['age']),
                    'reading_time': user_info['reading_time'],
                    'raw_books_per_year': books_per_year
                },
                'preferences': {
                    'liked_books': set(liked_books['book_id']),
                    'reading_patterns': reading_patterns
                }
            }
        except Exception as e:
            print(f"Erreur lors de la création du profil utilisateur {user_id}: {str(e)}")
            return None

    def _calculate_user_similarity(self, user1_profile, user2_profile):
        """
        Calcule une similarité enrichie entre utilisateurs
        """
        if user1_profile is None or user2_profile is None:
            return 0

        try:
            # Similarité d'âge avec fonction gaussienne
            age_diff = abs(user1_profile['demographic']['raw_age'] - user2_profile['demographic']['raw_age'])
            age_sim = np.exp(-age_diff**2 / 100)
            
            # Similarité de genre moins binaire
            gender_sim = 1 if user1_profile['demographic']['gender'] == user2_profile['demographic']['gender'] else 0.5
            
            # Similarité des livres avec bonus de diversité
            books1 = user1_profile['preferences']['liked_books']
            books2 = user2_profile['preferences']['liked_books']
            if not books1 or not books2:
                books_sim = 0
            else:
                intersection = len(books1.intersection(books2))
                union = len(books1.union(books2))
                diversity_bonus = min(1, len(books1) / 10) * min(1, len(books2) / 10)
                books_sim = ((intersection / union) * (1 + np.log1p(intersection))) * (1 + diversity_bonus)
                
            # Similarité des habitudes de lecture
            books_per_year_diff = abs(user1_profile['demographic']['raw_books_per_year'] - 
                                    user2_profile['demographic']['raw_books_per_year'])
            books_per_year_sim = np.exp(-books_per_year_diff**2 / 100)
            
            # Similarité du moment de lecture moins binaire
            reading_time_sim = 1 if (user1_profile['demographic']['reading_time'] == 
                                user2_profile['demographic']['reading_time']) else 0.7
            
            # Pondération dynamique
            weights = {
                'age': 0.15,
                'gender': 0.1,
                'books': 0.5,
                'books_per_year': 0.15,
                'reading_time': 0.1
            }
            
            similarity = (
                weights['age'] * age_sim +
                weights['gender'] * gender_sim +
                weights['books'] * books_sim +
                weights['books_per_year'] * books_per_year_sim +
                weights['reading_time'] * reading_time_sim
            )
            
            # Bruit aléatoire pour la diversité
            noise = np.random.normal(0, 0.05)
            similarity = max(0, min(1, similarity + noise))
            
            return similarity
                
        except Exception as e:
            print(f"Erreur lors du calcul de similarité: {str(e)}")
            return 0

    def _calculate_recommendation_score(self, similarity, book_id, current_recommendations, user_profile):
        """
        Calcule un score de recommandation avec plus de poids sur la diversité
        """
        base_score = similarity
        
        # Bonus pour popularité moyenne
        popularity = self.book_popularity.get(book_id, 0)
        popularity_bonus = 4 * popularity * (1 - popularity)
        
        # Score de diversité
        diversity_score = self.book_diversity_score.get(book_id, 0.5)
        
        # Pénalités pour répétitions
        diversity_penalty = 0
        recommendation_count = sum(1 for rec in current_recommendations if rec['book_id'] == book_id)
        if recommendation_count > 0:
            diversity_penalty = 0.3 * recommendation_count
        
        # Pénalité pour genres répétés
        genre_penalty = 0
        if 'genre' in self.books.columns:
            book_genre = self.books[self.books['book_id'] == book_id]['genre'].iloc[0]
            genre_count = sum(1 for rec in current_recommendations 
                            if self.books[self.books['book_id'] == rec['book_id']]['genre'].iloc[0] == book_genre)
            genre_penalty = 0.2 * genre_count
        
        # Nouvelle pondération favorisant la diversité
        weights = {
            'similarity': 0.35,
            'popularity': 0.15,
            'diversity': 0.35,
            'penalties': 0.15
        }
        
        final_score = (
            weights['similarity'] * base_score +
            weights['popularity'] * popularity_bonus +
            weights['diversity'] * diversity_score -
            weights['penalties'] * (diversity_penalty + genre_penalty)
        )
        
        # Facteur aléatoire contrôlé
        random_factor = np.random.uniform(0.95, 1.05)
        final_score *= random_factor
        
        return max(0, final_score)

    def get_recommendations(self, user_id, n_recommendations=3):
        """
        Génère des recommandations diverses avec historique
        """
        # Initialiser l'historique si nécessaire
        if user_id not in self.recommendation_history:
            self.recommendation_history[user_id] = set()
        
        target_profile = self._create_user_profile_vector(user_id)
        if target_profile is None:
            return []
        
        # Obtenir l'historique des recommandations
        user_history = self.recommendation_history[user_id]
        
        if not target_profile['preferences']['liked_books']:
            # Recommandations pour nouveaux utilisateurs
            popular_books = self.book_popularity.nlargest(n_recommendations * 6)
            diverse_recommendations = []
            
            for book_id, pop_score in popular_books.items():
                if book_id not in user_history:
                    diversity_score = self.book_diversity_score.get(book_id, 0.5)
                    combined_score = 0.6 * pop_score + 0.4 * diversity_score
                    book_info = self.books[self.books['book_id'] == book_id]
                    
                    if not book_info.empty:
                        diverse_recommendations.append({
                            'book_id': book_id,
                            'title': book_info.iloc[0]['book_title'],
                            'score': combined_score,
                            'type': 'découverte',
                            'genre': book_info.iloc[0].get('genre', 'unknown')
                        })
            
            diverse_recommendations.sort(key=lambda x: x['score'], reverse=True)
            final_recommendations = self._ensure_diversity(diverse_recommendations, n_recommendations)
            
            # Mettre à jour l'historique
            for rec in final_recommendations:
                user_history.add(rec['book_id'])
                
            return final_recommendations
        
        # Calcul des similarités utilisateurs
        user_similarities = []
        for other_user_id in self.users['user_id'].unique():
            if other_user_id != user_id:
                other_profile = self._create_user_profile_vector(other_user_id)
                if other_profile and other_profile['preferences']['liked_books']:
                    similarity = self._calculate_user_similarity(target_profile, other_profile)
                    if similarity > 0:
                        user_similarities.append((other_user_id, similarity))
        
        user_similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Générer les recommandations
        # Générer les recommandations
        recommendations = []
        seen_books = set()
        genres_counter = Counter()  # Utiliser un Counter au lieu d'un set
        
        for similar_user_id, similarity in user_similarities:
            if len(recommendations) >= n_recommendations * 4:
                break
                
            similar_user_books = set(self.liked_books[self.liked_books['user_id'] == similar_user_id]['book_id'])
            new_books = similar_user_books - target_profile['preferences']['liked_books'] - seen_books - user_history
            
            for book_id in new_books:
                book_info = self.books[self.books['book_id'] == book_id]
                if not book_info.empty:
                    book_genre = book_info.iloc[0].get('genre', 'unknown')
                    
                    # Limiter le nombre de livres par genre
                    if genres_counter[book_genre] >= 2:  # Utiliser le Counter
                        continue
                    
                    score = self._calculate_recommendation_score(
                        similarity, 
                        book_id, 
                        recommendations,
                        target_profile
                    )
                    
                    # Bonus pour la nouveauté
                    novelty_bonus = 0.1 if len(recommendations) < n_recommendations else 0
                    score += novelty_bonus
                    
                    recommendations.append({
                        'book_id': book_id,
                        'title': book_info.iloc[0]['book_title'],
                        'score': score,
                        'from_user': similar_user_id,
                        'type': 'personnalisée',
                        'genre': book_genre
                    })
                    seen_books.add(book_id)
                    genres_counter[book_genre] += 1  # Incrémenter le compteur
        
        # Trier par score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        # Sélectionner les recommandations finales avec diversité assurée
        final_recommendations = self._ensure_diversity(recommendations, n_recommendations)
        
        # Mettre à jour l'historique
        for rec in final_recommendations:
            user_history.add(rec['book_id'])
        
        # Limiter la taille de l'historique (garder les 20 dernières recommandations)
        if len(user_history) > 20:
            user_history = set(list(user_history)[-20:])
        
        return final_recommendations

    def _ensure_diversity(self, recommendations, n_recommendations):
        """
        Assure la diversité des recommandations finales
        """
        final_recommendations = []
        genres_count = Counter()
        
        for rec in recommendations:
            if len(final_recommendations) >= n_recommendations:
                break
                
            genre = rec.get('genre', 'unknown')
            
            # Vérifier les conditions de diversité
            similar_scores = sum(1 for f_rec in final_recommendations 
                               if abs(f_rec['score'] - rec['score']) < 0.05)  # Seuil strict
            
            max_genre_count = max(1, n_recommendations // 2)
            
            if (genres_count[genre] < max_genre_count and  # Limite par genre
                similar_scores < 1):  # Évite les scores trop similaires
                
                final_recommendations.append(rec)
                genres_count[genre] += 1
        
        return final_recommendations
