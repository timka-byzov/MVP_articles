import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  CircularProgress,
  Button,
  Alert
} from '@mui/material';
import ArticleCard from './ArticleCard';
import { feed, articles as articlesApi } from '../../services/api';

function FeedList() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [interactions, setInteractions] = useState({});

  const loadFeed = async (currentOffset = 0) => {
    try {
      setLoading(true);
      const response = await feed.get({ limit: 10, offset: currentOffset });
      const newArticles = response.data.articles;
      
      // Извлекаем interactions из статей
      const newInteractions = {};
      newArticles.forEach(article => {
        if (article.interactions) {
          newInteractions[article.id] = article.interactions;
        }
      });
      
      if (currentOffset === 0) {
        setArticles(newArticles);
        setInteractions(newInteractions);
      } else {
        setArticles(prev => [...prev, ...newArticles]);
        setInteractions(prev => ({ ...prev, ...newInteractions }));
      }
      
      setHasMore(newArticles.length === 10);
      setOffset(currentOffset + newArticles.length);
    } catch (err) {
      setError('Ошибка загрузки ленты');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFeed();
  }, []);

  const handleInteract = async (articleId, type) => {
    try {
      // Если скрываем статью, сразу удаляем из UI
      if (type === 'hide') {
        setArticles(prev => prev.filter(a => a.id !== articleId));
      }
      
      const response = await articlesApi.interact(articleId, type);
      
      // Обновляем локальное состояние взаимодействий (toggle)
      // Только для like и save, hide не нужен toggle
      if (type !== 'hide') {
        setInteractions(prev => {
          const current = prev[articleId] || {};
          const newState = { ...current };
          
          if (response.data.status === 'removed') {
            // Удаляем взаимодействие
            delete newState[type];
          } else {
            // Добавляем взаимодействие
            newState[type] = true;
          }
          
          return {
            ...prev,
            [articleId]: newState
          };
        });
      }
    } catch (err) {
      console.error('Ошибка взаимодействия:', err);
      // Если ошибка при скрытии, возвращаем статью обратно
      if (type === 'hide') {
        loadFeed(0); // Перезагружаем ленту
      }
    }
  };

  const handleLoadMore = () => {
    loadFeed(offset);
  };

  if (loading && articles.length === 0) {
    return (
      <Container maxWidth="md">
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Персональная лента
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {articles.length === 0 ? (
          <Alert severity="info">
            Статьи не найдены. Попробуйте изменить предпочтения.
          </Alert>
        ) : (
          <>
            {articles.map((article) => (
              <ArticleCard
                key={article.id}
                article={article}
                onInteract={handleInteract}
                interactions={interactions[article.id] || {}}
              />
            ))}

            {hasMore && (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
                <Button
                  variant="outlined"
                  onClick={handleLoadMore}
                  disabled={loading}
                >
                  {loading ? 'Загрузка...' : 'Загрузить ещё'}
                </Button>
              </Box>
            )}
          </>
        )}
      </Box>
    </Container>
  );
}

export default FeedList;