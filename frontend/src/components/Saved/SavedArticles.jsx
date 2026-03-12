import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  CircularProgress,
  Alert
} from '@mui/material';
import ArticleCard from '../Feed/ArticleCard';
import { articles as articlesApi } from '../../services/api';

function SavedArticles() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [interactions, setInteractions] = useState({});

  const loadSavedArticles = async () => {
    try {
      setLoading(true);
      const response = await articlesApi.getSaved();
      const savedArticles = response.data.articles;
      
      // Все статьи уже сохранены, устанавливаем interactions
      const newInteractions = {};
      savedArticles.forEach(article => {
        newInteractions[article.id] = {
          save: true,
          ...(article.interactions || {})
        };
      });
      
      setArticles(savedArticles);
      setInteractions(newInteractions);
    } catch (err) {
      setError('Ошибка загрузки избранного');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSavedArticles();
  }, []);

  const handleInteract = async (articleId, type) => {
    try {
      // Запрещаем скрытие и повторное сохранение
      if (type === 'hide') {
        return; // Игнорируем
      }
      
      if (type === 'save') {
        // Убираем из избранного
        await articlesApi.interact(articleId, type);
        // Удаляем статью из списка
        setArticles(prev => prev.filter(a => a.id !== articleId));
        return;
      }
      
      // Для like - обычный toggle
      const response = await articlesApi.interact(articleId, type);
      
      setInteractions(prev => {
        const current = prev[articleId] || {};
        const newState = { ...current };
        
        if (response.data.status === 'removed') {
          delete newState[type];
        } else {
          newState[type] = true;
        }
        
        return {
          ...prev,
          [articleId]: newState
        };
      });
    } catch (err) {
      console.error('Ошибка взаимодействия:', err);
    }
  };

  if (loading) {
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
          Избранное
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {articles.length === 0 ? (
          <Alert severity="info">
            У вас пока нет сохраненных статей
          </Alert>
        ) : (
          <>
            {articles.map((article) => (
              <ArticleCard
                key={article.id}
                article={article}
                onInteract={handleInteract}
                interactions={interactions[article.id] || {}}
                hideSaveButton={false}
                hideHideButton={true}
              />
            ))}
          </>
        )}
      </Box>
    </Container>
  );
}

export default SavedArticles;