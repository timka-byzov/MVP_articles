import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  IconButton,
  Chip,
  Box,
  Link as MuiLink
} from '@mui/material';
import {
  Favorite,
  FavoriteBorder,
  BookmarkAdd,
  BookmarkAdded,
  VisibilityOff,
  OpenInNew
} from '@mui/icons-material';

function ArticleCard({ article, onInteract, interactions = {}, hideHideButton = false, hideSaveButton = false }) {
  const isLiked = interactions.like;
  const isSaved = interactions.save;

  const handleInteract = (type) => {
    onInteract(article.id, type);
  };

  return (
    <Card sx={{ mb: 2, '&:hover': { boxShadow: 6 } }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
          {article.title}
        </Typography>
        
        <Typography variant="body2" color="text.secondary" paragraph>
          {article.summary}
        </Typography>

        <Box sx={{ mb: 1 }}>
          <Typography variant="caption" color="text.secondary">
            {article.authors?.map(a => a.name).join(', ')} • {article.source} • {article.publication_date}
          </Typography>
        </Box>

        {article.topics && article.topics.length > 0 && (
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 1 }}>
            {article.topics.map((topic, idx) => (
              <Chip
                key={idx}
                label={topic}
                size="small"
                variant="outlined"
              />
            ))}
          </Box>
        )}

        {article.url && (
          <Box sx={{ mt: 2 }}>
            <MuiLink
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              sx={{ display: 'inline-flex', alignItems: 'center', gap: 0.5 }}
            >
              Читать статью <OpenInNew fontSize="small" />
            </MuiLink>
          </Box>
        )}
      </CardContent>
      
      <CardActions sx={{ justifyContent: 'space-between', px: 2, pb: 2 }}>
        <Box>
          <IconButton
            onClick={() => handleInteract('like')}
            color={isLiked ? 'error' : 'default'}
            title="Нравится"
          >
            {isLiked ? <Favorite /> : <FavoriteBorder />}
          </IconButton>
          
          {!hideSaveButton && (
            <IconButton
              onClick={() => handleInteract('save')}
              color={isSaved ? 'primary' : 'default'}
              title={isSaved ? "Убрать из избранного" : "Сохранить"}
            >
              {isSaved ? <BookmarkAdded /> : <BookmarkAdd />}
            </IconButton>
          )}
        </Box>

        {!hideHideButton && (
          <IconButton
            onClick={() => handleInteract('hide')}
            title="Скрыть"
            size="small"
          >
            <VisibilityOff />
          </IconButton>
        )}
      </CardActions>
    </Card>
  );
}

export default ArticleCard;