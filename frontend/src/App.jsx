import React, { useState, useEffect } from 'react';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import Header from './components/Layout/Header';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import TopicSelector from './components/Onboarding/TopicSelector';
import FeedList from './components/Feed/FeedList';
import SavedArticles from './components/Saved/SavedArticles';
import { auth, preferences } from './services/api';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showRegister, setShowRegister] = useState(false);
  const [needsOnboarding, setNeedsOnboarding] = useState(false);
  const [currentPage, setCurrentPage] = useState('feed'); // 'feed' or 'saved'

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await auth.me();
      setUser(response.data);
      
      // Проверяем, есть ли у пользователя предпочтения
      const prefsResponse = await preferences.get();
      if (prefsResponse.data.preferences.length === 0) {
        setNeedsOnboarding(true);
      }
    } catch (err) {
      // Пользователь не авторизован
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = () => {
    checkAuth();
  };

  const handleRegister = () => {
    setNeedsOnboarding(true);
    checkAuth();
  };

  const handleLogout = async () => {
    try {
      await auth.logout();
      setUser(null);
      setNeedsOnboarding(false);
    } catch (err) {
      console.error('Logout error:', err);
    }
  };

  const handleOnboardingComplete = () => {
    setNeedsOnboarding(false);
  };

  if (loading) {
    return null;
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      
      {user && (
        <Header
          user={user}
          onLogout={handleLogout}
          currentPage={currentPage}
          onNavigate={setCurrentPage}
        />
      )}
      
      {!user ? (
        showRegister ? (
          <Register
            onRegister={handleRegister}
            onSwitchToLogin={() => setShowRegister(false)}
          />
        ) : (
          <Login
            onLogin={handleLogin}
            onSwitchToRegister={() => setShowRegister(true)}
          />
        )
      ) : needsOnboarding ? (
        <TopicSelector onComplete={handleOnboardingComplete} />
      ) : currentPage === 'saved' ? (
        <SavedArticles />
      ) : (
        <FeedList />
      )}
    </ThemeProvider>
  );
}

export default App;