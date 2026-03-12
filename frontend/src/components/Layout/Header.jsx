import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box
} from '@mui/material';
import { Logout } from '@mui/icons-material';

function Header({ user, onLogout, currentPage, onNavigate }) {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 1, cursor: 'pointer' }}
          onClick={() => onNavigate('feed')}
        >
          MVP Articles
        </Typography>
        
        {user && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Button
              color="inherit"
              onClick={() => onNavigate('feed')}
              variant={currentPage === 'feed' ? 'outlined' : 'text'}
            >
              Лента
            </Button>
            <Button
              color="inherit"
              onClick={() => onNavigate('saved')}
              variant={currentPage === 'saved' ? 'outlined' : 'text'}
            >
              Избранное
            </Button>
            <Typography variant="body2">
              {user.full_name || user.email}
            </Typography>
            <Button
              color="inherit"
              startIcon={<Logout />}
              onClick={onLogout}
            >
              Выйти
            </Button>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
}

export default Header;