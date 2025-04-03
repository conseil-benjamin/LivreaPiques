from application_system_reco.SQL_controleur.SQL_controleur import *
from application_system_reco.api import *
import asyncio
import json
import os
import time

# Définition de la classe UserID
class UserID(BaseModel):
    id: int

class FinalPrediction:
    def __init__(self):
        """
            Initialise le système de prédiction avec les données de Supabase.
        """
        try:
            self.prediction_list = {}
            self.cache_file = 'application_system_reco/caches/sales_predictions.json'
            self.cache_duration = 24 * 3600  # 24 heures en secondes
            
            # Tente de charger les prédictions depuis le cache
            if self._load_cache():
                print("Prédictions chargées depuis le cache")
        except Exception as e:
            print(f"Error initializing FinalPrediction: {str(e)}")
            raise

    def _load_cache(self):
        """Charge les prédictions depuis le cache si celui-ci existe et est valide"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                    
                    # Vérifie si le cache contient un timestamp
                    if isinstance(cache_data, dict) and "timestamp" in cache_data:
                        cache_age = time.time() - cache_data["timestamp"]
                        if cache_age < self.cache_duration:
                            self.prediction_list = cache_data["predictions"]
                            return True
                    else:
                        # Si c'est l'ancien format, on le considère comme invalide
                        return False
            return False
        except Exception as e:
            print(f"Erreur lors du chargement du cache: {str(e)}")
            return False

    def _save_cache(self):
        """Sauvegarde les prédictions dans le cache avec le timestamp actuel"""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            # On sauvegarde le timestamp avec les données
            cache_data = {
                "timestamp": time.time(),
                "predictions": self.prediction_list
            }
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du cache: {str(e)}")

    def _get_recommendations_data(self, users):            
        try:
            engine, session, schema = conexion_db()

            for user_id in users:
                try:
                    user_id = UserID(id=user_id)
                    
                    # Use synchronous recommendation functions
                    reco1_result = recommendation1_sync(user_id)
                    reco2_result = recommendation2_sync(user_id)

                    # On ajoute un poids à chaque livre recommandé
                    for book_id in reco1_result["recommendations"]:
                        if book_id not in self.prediction_list:
                            self.prediction_list[book_id] = 2
                        else:
                            self.prediction_list[book_id] += 2

                    for book_id in reco2_result["recommendations"]:
                        if book_id not in self.prediction_list:
                            self.prediction_list[book_id] = 1
                        else:
                            self.prediction_list[book_id] += 1                    
                except Exception as e:
                    print(f"Error getting recommendations for user {user_id}: {str(e)}")
                    continue
            
            return self.prediction_list

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Erreur de base de données: {str(e)}")
        finally:
            session.close()

    def _get_wishlist_data(self, users):
        """Récupère les livres dans la wishlist de chaque utilisateur"""
        try:
            engine, session, schema = conexion_db()

            for user_id in users:
                try:
                    query = text("""
                        SELECT book_id FROM wishlist 
                        WHERE user_id = :user_id
                    """)
                    wishlist_books = session.execute(query, {"user_id": user_id}).fetchall()

                    # Ajouter un poids de 3 pour chaque livre
                    for book in wishlist_books:
                        book_id = book[0]
                        if book_id not in self.prediction_list:
                            self.prediction_list[book_id] = 3
                        else:
                            self.prediction_list[book_id] += 3

                except Exception as e:
                    print(f"Error processing wishlist for user {user_id}: {str(e)}")
                    continue


        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Erreur de base de données: {str(e)}")
        finally:
            session.close()

    def _calculate_most_reading_users(self, n):
        """
            Détermine les habitudes de lecture des utilisateurs et retourne les n plus assidus.

            :param n: Le nombre d'utilisateurs à retourner
            :return: Liste d'utilisateurs les plus assidus
        """
        try:
            engine, session, schema = conexion_db()
            readers = {}

            query = text("""
                SELECT user_id FROM "user" 
                WHERE user_type = 'user'
            """)
            users = session.execute(query).fetchall()

            for user in users:
                user_id = user[0]

                # Reading frequency weight
                query = text("""
                    SELECT nb_book_per_year FROM "user" 
                    WHERE user_id = :user_id
                """)
                read_infos = session.execute(query, {'user_id': user_id}).fetchone()

                reading_frequency_map = {
                    '0': 0,
                    '1 à 5': 3,
                    '6 à 10': 8,
                    '11 à 20': 15,
                    'plus de 20': 25,
                    None: 0
                }
                frequency_weight = reading_frequency_map.get(read_infos[0], 0) if read_infos else 0

                # Read books weight
                query = text("""
                    SELECT COUNT(*) FROM read_books 
                    WHERE user_id = :user_id
                """)
                read_books = session.execute(query, {'user_id': user_id}).fetchone()
                read_weight = read_books[0] * 2 if read_books else 0

                # Liked books weight
                query = text("""
                    SELECT COUNT(*) FROM liked_books 
                    WHERE user_id = :user_id
                """)
                liked_books = session.execute(query, {'user_id': user_id}).fetchone()
                liked_weight = liked_books[0] * 3 if liked_books else 0

                # Calculate total weight for user
                total_weight = frequency_weight + read_weight + liked_weight
                readers[user_id] = total_weight

            # Sort readers by weight and get top n users as a list
            top_readers = sorted(readers.items(), key=lambda x: x[1], reverse=True)[:n]
            top_readers = [user_id for user_id, weight in top_readers]
            return top_readers

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Erreur de base de données: {str(e)}")
        finally:
            session.close()

    def get_predictions(self):
        """Retourne les prédictions en les calculant si nécessaire"""
        if self._load_cache():
            # Pas de normalisation ici non plus
            return self.prediction_list

        readers = self._calculate_most_reading_users(10)
        self._get_recommendations_data(readers)
        self._get_wishlist_data(readers)
        # Normalisation uniquement à la fin de tous les calculs
        self._normalize_prediction_list()
        self._save_cache()
        return self.prediction_list
        
    def _normalize_prediction_list(self):
        """
        Normalise la liste de livres prédites.
        Les scores seront entre 0.1 et 1, avec possibilité d'avoir plusieurs livres à 1.
        """
        if self.prediction_list:
            max_score = max(self.prediction_list.values())
            # Ajuste les scores pour que le maximum soit à 1
            if max_score > 0:  # Évite la division par zéro
                self.prediction_list = {
                    k: max(0.1, min(1, v / max_score))
                    for k, v in self.prediction_list.items()
                }

# On intègre du code de api.py pour le réutiliser
def Ltitle_to_Lid(Ltitle):
    LrecoID = []
    for title in Ltitle:
        # Remplacement des ' uniquement pour le titre en cours
        safe_title = title.replace("'", "''")

        result = requete(f"""select book_id from book where book_title = '{safe_title}' """, True, False)
        
        if result.empty:  # Vérification pour éviter l'erreur "out-of-bounds"
            print(f"Erreur : Aucun résultat trouvé pour le titre '{title}'")
            continue
        
        LrecoID.append(int(result["book_id"].iloc[0]))
    return LrecoID

def recommendation1_sync(user: UserID):
    """
    Synchronous version of recommendation1.
    """
    try:
        engine, session, schema = conexion_db()
        excluded_query = text("""
            SELECT book_id FROM (
                SELECT book_id FROM liked_books WHERE user_id = :user_id
                UNION
                SELECT book_id FROM wishlist WHERE user_id = :user_id
                UNION
                SELECT book_id FROM read_books WHERE user_id = :user_id
            ) as excluded
        """)
        excluded_books = {
            book[0] for book in 
            session.execute(excluded_query, {"user_id": user.id}).fetchall()
        }
        
        reco_benj = FinalRecommender()
        initial_reco = reco_benj.get_recommendations(
            user_id=user.id,
            n_recommendations=15,
            excluded_books=excluded_books
        )
        
        final_reco = initial_reco[:5]
        
        if len(final_reco) < 5:
            additional_reco = reco_benj.get_recommendations(
                user_id=user.id,
                n_recommendations=10,
                excluded_books=excluded_books
            )
            additional_filtered = [
                book for book in additional_reco 
                if book["book_id"] not in [b["book_id"] for b in final_reco]
            ]
            final_reco.extend(additional_filtered[:5 - len(final_reco)])

        Ltitles = [book["title"] for book in final_reco]
        LrecoID = Ltitle_to_Lid(Ltitles)
        
        return {"recommendations": LrecoID}
        
    except Exception as e:
        print(f"Error in recommendation1_sync: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )
    finally:
        session.close()

def recommendation2_sync(user: UserID):
    """
    Synchronous version of recommendation2.
    """
    try:
        Lreco = reco_esteban(user.id) 
        LrecoID = Ltitle_to_Lid(Lreco)
        return {"recommendations": LrecoID}
    except Exception as e:
        print(f"Error in recommendation2_sync: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )
