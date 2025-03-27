import pandas as pd
import numpy as np
from supabase import create_client 
from sklearn.preprocessing import MinMaxScaler
from collections import Counter
from application_system_reco.SQL_controleur.SQL_controleur import *

class FinalRecommender:
    def __init__(self):
        """
            Initialise le système de recommandation avec les données de Supabase.
        """
        try:
            # Initialize MinMaxScaler first
            self.scaler = MinMaxScaler(feature_range=(0, 1))
            
            # Load data
            self.liked_books = requete("SELECT * FROM liked_books ORDER BY book_id")
            self.books = requete("SELECT * FROM book ORDER BY book_id")
            self.users = requete('''SELECT * FROM "user"''')

            # Convert nb_of_pages to numeric first
            self.books['nb_of_pages'] = pd.to_numeric(self.books['nb_of_pages'], errors='coerce')
            
            # Calculate default values
            default_pages = self.books['nb_of_pages'].median()  # Use median instead of mean for robustness
            
            # Handle missing values
            self.books = self.books.fillna({
                'book_rating': 0,
                'nb_of_pages': default_pages,
                'genre': 'unknown',
                'authors': 'unknown',
                'book_description': '',
                'book_cover': ''
            })
            
            # Initialize numeric features
            numeric_features = ['book_rating', 'nb_of_pages']
            for feature in numeric_features:
                if feature in self.books.columns:
                    self.books[feature] = pd.to_numeric(self.books[feature], errors='coerce').fillna(0)
            
            # Initialize recommendation history
            self.recommendation_history = {}
            
            # Calculate derived metrics
            self.book_popularity = self._calculate_book_popularity()
            self.user_reading_patterns = self._calculate_user_reading_patterns()
            self.book_diversity_score = self._calculate_book_diversity_scores()
            
            # Print dataset statistics
            print(f"Nombre total de livres : {len(self.books)}")
            print(f"Nombre total d'utilisateurs : {len(self.users)}")
            print(f"Nombre total de likes : {len(self.liked_books)}")
            
        except Exception as e:
            print(f"Error initializing FinalRecommender: {str(e)}")
            raise

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

        # Add NaN handling for numeric features
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        
        # Replace NaN values with defaults
        self.books = self.books.fillna({
            'book_rating': 0,
            'nb_of_pages': self.books['nb_of_pages'].mean(),
            'genres': 'unknown',
            'authors': 'unknown'
        })
        
        # Initialize numeric features properly
        numeric_features = self.books.select_dtypes(include=['float64', 'int64']).columns
        self.books[numeric_features] = self.books[numeric_features].fillna(0)

    def _create_user_profile_vector(self, user_id):
        """
        Crée un profil utilisateur enrichi avec patterns de lecture
        """
        try:
            user_matches = self.users[self.users['user_id'] == user_id]
            if user_matches.empty:
                return None
                
            user_info = user_matches.iloc[0]
            
            # Handle missing values in user data
            age = float(user_info['age']) if pd.notna(user_info['age']) else 30.0
            books_per_year = self._convert_book_range(user_info['nb_book_per_year']) if pd.notna(user_info['nb_book_per_year']) else 5
            
            # Scale features individually to avoid NaN propagation
            age_scaled = self.scaler.fit_transform([[age]])[0][0] if age > 0 else 0.5
            books_scaled = self.scaler.fit_transform([[books_per_year]])[0][0] if books_per_year > 0 else 0.5
            
            return {
                'demographic': {
                    'age': age_scaled,
                    'gender': 1 if user_info['gender'] == 'M' else 0,
                    'books_per_year': books_scaled
                },
                'preferences': {
                    'liked_books': set(self.liked_books[self.liked_books['user_id'] == user_id]['book_id']),
                    'reading_patterns': self.user_reading_patterns.get(user_id, {})
                }
            }
        except Exception as e:
            print(f"Error creating user profile: {str(e)}")
            return None

    def _calculate_user_similarity(self, user1_profile, user2_profile):
        """
        Calcule une similarité enrichie entre utilisateurs
        """
        if user1_profile is None or user2_profile is None:
            return 0

        try:
            # Similarité d'âge avec fonction gaussienne
            age1 = user1_profile['demographic']['age']
            age2 = user2_profile['demographic']['age']
            age_diff = abs(age1 - age2)
            age_sim = np.exp(-age_diff**2 / 100)
            
            # Similarité de genre
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
            books_per_year1 = user1_profile['demographic']['books_per_year']
            books_per_year2 = user2_profile['demographic']['books_per_year']
            books_per_year_diff = abs(books_per_year1 - books_per_year2)
            books_per_year_sim = np.exp(-books_per_year_diff**2 / 100)
            
            # Pondération dynamique
            weights = {
                'age': 0.15,
                'gender': 0.1,
                'books': 0.6,
                'books_per_year': 0.15
            }
            
            similarity = (
                weights['age'] * age_sim +
                weights['gender'] * gender_sim +
                weights['books'] * books_sim +
                weights['books_per_year'] * books_per_year_sim
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

    def get_recommendations(self, user_id, n_recommendations=5, excluded_books=None):
        """
        Génère des recommandations uniques en excluant les livres déjà lus, likés ou wishlistés
        """
        try:
            # Initialize recommendation history
            if user_id not in self.recommendation_history:
                self.recommendation_history[user_id] = set()
            
            # Get user profile
            target_profile = self._create_user_profile_vector(user_id)
            if target_profile is None:
                print(f"No profile found for user {user_id}")
                return []
            
            # Use provided excluded_books or create empty set
            excluded_books = excluded_books or set()
            
            # Add previously recommended books to exclusions
            excluded_books.update(self.recommendation_history[user_id])
            
            print(f"Total excluded books for user {user_id}: {len(excluded_books)}")
            
            # Get available books (not in excluded list)
            available_books = self.books[~self.books['book_id'].isin(excluded_books)]
            print(f"Available books after filtering: {len(available_books)}")
        
            if available_books.empty:
                print("No available books after filtering")
                return []
            
            # Discovery approach for new users
            if not target_profile['preferences']['liked_books']:
                all_book_candidates = []
                available_books = self.books[~self.books['book_id'].isin(excluded_books)]
                
                for _, book in available_books.iterrows():
                    pop_score = self.book_popularity.get(book['book_id'], 0)
                    diversity_score = self.book_diversity_score.get(book['book_id'], 0.5)
                    combined_score = 0.6 * pop_score + 0.4 * diversity_score
                    
                    all_book_candidates.append({
                        'book_id': book['book_id'],
                        'title': book['book_title'],
                        'score': combined_score,
                        'type': 'découverte',
                        'genre': book.get('genre', 'unknown')
                    })
                
                # Sort and ensure diversity
                all_book_candidates.sort(key=lambda x: x['score'], reverse=True)
                recommendations = self.ensure_diversity(all_book_candidates, n_recommendations)
                
                # Update history
                for rec in recommendations:
                    self.recommendation_history[user_id].add(rec['book_id'])
                    
                return recommendations

            # Collaborative approach for existing users
            user_similarities = []
            for other_user_id in self.users['user_id'].unique():
                if other_user_id != user_id:
                    other_profile = self._create_user_profile_vector(other_user_id)
                    if other_profile and other_profile['preferences']['liked_books']:
                        similarity = self._calculate_user_similarity(target_profile, other_profile)
                        if similarity > 0:
                            user_similarities.append((other_user_id, similarity))
            
            user_similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Get recommendations from similar users
            all_recommendations = []
            available_books = self.books[~self.books['book_id'].isin(excluded_books)]
            
            for _, book in available_books.iterrows():
                max_similarity = max([sim for _, sim in user_similarities], default=0)
                score = self._calculate_recommendation_score(
                    max_similarity,
                    book['book_id'],
                    all_recommendations,
                    target_profile
                )
                
                all_recommendations.append({
                    'book_id': book['book_id'],
                    'title': book['book_title'],
                    'score': score,
                    'type': 'personnalisée',
                    'genre': book.get('genre', 'unknown')
                })
            
            # Sort and ensure diversity
            all_recommendations.sort(key=lambda x: x['score'], reverse=True)
            recommendations = self.ensure_diversity(all_recommendations, n_recommendations)
            
            # Update history
            for rec in recommendations:
                self.recommendation_history[user_id].add(rec['book_id'])
            
            return recommendations

        except Exception as e:
            print(f"Error getting recommendations for user {user_id}: {str(e)}")
            return []

    def ensure_diversity(self, recommendations, n_recommendations=5):
        if len(recommendations) == 0:
            return []
        
        final_recommendations = []
        used_book_ids = set()
        genres_count = Counter()
        
        # Trier les recommandations par score pour prioriser les meilleures
        recommendations_sorted = sorted(recommendations, key=lambda x: x['score'], reverse=True)
        
        # Premier passage - sélection avec critères stricts
        for rec in recommendations_sorted:
            if len(final_recommendations) >= n_recommendations:
                break
            
            # Vérifier que le livre n'a pas déjà été recommandé
            if rec['book_id'] in used_book_ids:
                continue
            
            genre = rec.get('genre', 'unknown')
            max_genre_count = max(1, n_recommendations // 2)
            
            # Vérifier la diversité des genres
            if genres_count[genre] < max_genre_count:
                final_recommendations.append(rec)
                used_book_ids.add(rec['book_id'])
                genres_count[genre] += 1
        
        # Deuxième passage - compléter jusqu'à n_recommendations
        if len(final_recommendations) < n_recommendations:
            for rec in recommendations_sorted:
                if len(final_recommendations) >= n_recommendations:
                    break
                
                # Ajouter uniquement les livres pas encore recommandés
                if rec['book_id'] not in used_book_ids:
                    final_recommendations.append(rec)
                    used_book_ids.add(rec['book_id'])
        
        # Si toujours pas assez de recommandations, lever une exception
        if len(final_recommendations) < n_recommendations:
            raise ValueError(f"Impossible de générer {n_recommendations} recommandations uniques")
        
        return final_recommendations[:n_recommendations]