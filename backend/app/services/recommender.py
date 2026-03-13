from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
from typing import List
from uuid import UUID


class TFIDFRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.tfidf_matrix = None
        self.article_ids = []
    
    def fit(self, articles: List):
        """Обучить на корпусе статей"""
        texts = [f"{a.title} {a.abstract}" for a in articles]
        self.article_ids = [a.id for a in articles]
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)
        return self
    
    def get_vector(self, text: str) -> np.ndarray:
        """Получить TF-IDF вектор для текста"""
        return self.vectorizer.transform([text]).toarray()[0]
    
    def serialize_vector(self, vector: np.ndarray) -> str:
        """Сериализовать вектор в строку"""
        return pickle.dumps(vector).hex()
    
    def deserialize_vector(self, vector_str: str) -> np.ndarray:
        """Десериализовать вектор из строки"""
        return pickle.loads(bytes.fromhex(vector_str))
    
    def build_user_profile(
        self,
        interactions: List[tuple],
        preferences: List
    ) -> np.ndarray:
        """Построить профиль пользователя из кортежей (interaction, article)"""
        # Определяем размерность векторов
        if self.tfidf_matrix is None:
            raise ValueError("Recommender not fitted. Call fit() first.")
        
        vector_size = self.tfidf_matrix.shape[1]
        weighted_vectors = []
        
        # Веса для типов взаимодействий
        weights = {
            'like': 1.0,
            'save': 0.8,
            'view': 0.3,
            'hide': -0.5
        }
        
        # Добавляем векторы из взаимодействий
        for interaction, article in interactions:
            if article and article.tfidf_vector:
                try:
                    vector = self.deserialize_vector(article.tfidf_vector)
                    # Проверяем размерность
                    if len(vector) == vector_size:
                        weight = weights.get(interaction.interaction_type.value, 0.5)
                        weighted_vectors.append(vector * weight)
                except Exception as e:
                    print(f"Warning: Failed to deserialize vector for article {article.id}: {e}")
                    continue
        
        # Добавляем векторы из предпочтений
        for pref in preferences:
            try:
                topic_vector = self.get_vector(pref.topic)
                # Проверяем размерность
                if len(topic_vector) == vector_size:
                    weighted_vectors.append(topic_vector * pref.weight)
            except Exception as e:
                print(f"Warning: Failed to get vector for topic {pref.topic}: {e}")
                continue
        
        if not weighted_vectors:
            # Если нет данных, возвращаем нулевой вектор
            return np.zeros(vector_size)
        
        # Преобразуем в numpy array и вычисляем среднее
        weighted_vectors = np.array(weighted_vectors)
        return np.mean(weighted_vectors, axis=0)
    
    def recommend(
        self,
        user_profile: np.ndarray,
        n: int = 20,
        exclude_ids: List[UUID] = None,
        exploration_rate: float = 0.1
    ) -> List[UUID]:
        """Получить рекомендации"""
        if exclude_ids is None:
            exclude_ids = []
        
        print(f"DEBUG RECOMMENDER: exclude_ids = {exclude_ids}")
        print(f"DEBUG RECOMMENDER: article_ids = {self.article_ids}")
        
        # Вычисляем сходство
        similarities = cosine_similarity(
            user_profile.reshape(1, -1),
            self.tfidf_matrix
        )[0]
        
        # Создаем маску для исключенных статей
        mask = np.ones(len(similarities), dtype=bool)
        excluded_count = 0
        for i, article_id in enumerate(self.article_ids):
            if article_id in exclude_ids:
                mask[i] = False
                excluded_count += 1
        
        print(f"DEBUG RECOMMENDER: excluded {excluded_count} articles")
        print(f"DEBUG RECOMMENDER: mask = {mask}")
        
        # Применяем маску
        filtered_similarities = similarities.copy()
        filtered_similarities[~mask] = -np.inf
        
        # Проверяем, есть ли доступные статьи
        available_indices = np.where(mask)[0]
        if len(available_indices) == 0:
            # Все статьи исключены
            return []
        
        # Exploitation: топ статьи по релевантности
        n_exploit = int(n * (1 - exploration_rate))
        # Берем только из доступных индексов
        sorted_indices = np.argsort(filtered_similarities)[::-1]
        # Фильтруем только те, которые не -inf
        valid_indices = [i for i in sorted_indices if filtered_similarities[i] > -np.inf]
        top_indices = valid_indices[:n_exploit]
        
        # Exploration: случайные статьи
        n_explore = n - len(top_indices)
        if n_explore > 0 and len(available_indices) > len(top_indices):
            # Исключаем уже выбранные в exploitation
            remaining = [i for i in available_indices if i not in top_indices]
            if len(remaining) > 0:
                explore_indices = np.random.choice(
                    remaining,
                    size=min(n_explore, len(remaining)),
                    replace=False
                )
            else:
                explore_indices = np.array([])
        else:
            explore_indices = np.array([])
        
        # Объединяем
        all_indices = np.concatenate([top_indices, explore_indices])
        
        return [self.article_ids[int(i)] for i in all_indices]