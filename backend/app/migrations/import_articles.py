import json
import sys
from sqlmodel import Session, select
from app.database import sync_engine
from app.models.article import Article
from app.services.recommender import TFIDFRecommender
from app.services.recommender_cache import RecommenderCache
from datetime import datetime
import argparse


def import_articles(json_path: str = "/data/articles.json", clean: bool = False):
    """Импортировать статьи из JSON"""
    
    print(f"Loading articles from {json_path}...")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File {json_path} not found!")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format: {e}")
        sys.exit(1)
    
    articles_data = data.get('articles', [])
    print(f"Found {len(articles_data)} articles")
    
    if not articles_data:
        print("No articles to import!")
        return
    
    with Session(sync_engine) as session:
        # Очистка если нужно
        if clean:
            print("Cleaning existing articles...")
            for article in session.exec(select(Article)).all():
                session.delete(article)
            session.commit()
            print("Existing articles deleted")
        
        # Создаем статьи
        articles = []
        for item in articles_data:
            try:
                article = Article(
                    title=item['title'],
                    abstract=item['abstract'],
                    summary=item['summary'],
                    authors=item['authors'],
                    source=item['source'],
                    doi=item.get('doi'),
                    publication_date=datetime.strptime(
                        item['publication_date'], '%Y-%m-%d'
                    ).date(),
                    topics=item.get('topics', []),
                    url=item.get('url')
                )
                articles.append(article)
            except KeyError as e:
                print(f"Warning: Skipping article due to missing field: {e}")
                continue
            except Exception as e:
                print(f"Warning: Error processing article: {e}")
                continue
        
        if not articles:
            print("No valid articles to import!")
            return
        
        # Вычисляем TF-IDF векторы
        print("Computing TF-IDF vectors...")
        recommender = TFIDFRecommender()
        recommender.fit(articles)
        
        # Сохраняем векторы и статьи
        print("Saving articles to database...")
        for i, article in enumerate(articles):
            vector = recommender.tfidf_matrix[i].toarray()[0]
            article.tfidf_vector = recommender.serialize_vector(vector)
            session.add(article)
        
        session.commit()
        print(f"✓ Successfully imported {len(articles)} articles")
        
        # Сбрасываем кэш рекомендателя
        RecommenderCache.invalidate()
        print("✓ Recommender cache invalidated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import articles from JSON file')
    parser.add_argument('--file', default='/data/articles.json', help='Path to JSON file')
    parser.add_argument('--clean', action='store_true', help='Clean existing articles before import')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()
    
    import_articles(args.file, args.clean)