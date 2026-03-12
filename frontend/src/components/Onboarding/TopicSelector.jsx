import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Chip,
  Button,
  Alert
} from '@mui/material';
import { preferences } from '../../services/api';

const AVAILABLE_TOPICS = [
  'machine learning',
  'deep learning',
  'natural language processing',
  'computer vision',
  'reinforcement learning',
  'neural networks',
  'transformers',
  'generative models',
  'optimization',
  'robotics',
  'data science',
  'artificial intelligence'
];

function TopicSelector({ onComplete }) {
  const [selectedTopics, setSelectedTopics] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleToggleTopic = (topic) => {
    if (selectedTopics.includes(topic)) {
      setSelectedTopics(selectedTopics.filter(t => t !== topic));
    } else {
      setSelectedTopics([...selectedTopics, topic]);
    }
  };

  const handleSubmit = async () => {
    if (selectedTopics.length === 0) {
      setError('Выберите хотя бы одну тему');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const topics = selectedTopics.map(topic => ({
        topic,
        weight: 1.0
      }));
      await preferences.set(topics);
      onComplete();
    } catch (err) {
      setError('Ошибка сохранения предпочтений');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 8 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center">
            Выберите интересующие темы
          </Typography>
          
          <Typography variant="body1" color="text.secondary" align="center" sx={{ mb: 4 }}>
            Выберите темы, которые вас интересуют, чтобы мы могли подобрать релевантные статьи
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 4 }}>
            {AVAILABLE_TOPICS.map((topic) => (
              <Chip
                key={topic}
                label={topic}
                onClick={() => handleToggleTopic(topic)}
                color={selectedTopics.includes(topic) ? 'primary' : 'default'}
                variant={selectedTopics.includes(topic) ? 'filled' : 'outlined'}
                sx={{ fontSize: '1rem', py: 2.5 }}
              />
            ))}
          </Box>

          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Выбрано: {selectedTopics.length}
            </Typography>
            
            <Button
              variant="contained"
              size="large"
              onClick={handleSubmit}
              disabled={loading || selectedTopics.length === 0}
            >
              {loading ? 'Сохранение...' : 'Продолжить'}
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}

export default TopicSelector;