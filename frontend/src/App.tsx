import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { useEffect } from 'react';
import { SessionManager } from './utils/sessionManager';

// Pages
import Dashboard from './pages/Dashboard';
import BusinessProfile from './pages/BusinessProfile';
import FinancialData from './pages/FinancialData';
import Assessment from './pages/Assessment';
import AssessmentList from './pages/AssessmentList';
import Reports from './pages/Reports';

// Components
import Layout from './components/Layout';

// Theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  // Initialize session on app load
  useEffect(() => {
    const session = SessionManager.getSession();
    console.log('Session initialized:', session.sessionId);
    
    // Check session expiry every minute
    const interval = setInterval(() => {
      if (SessionManager.isSessionExpired()) {
        console.log('Session expired, clearing data...');
        SessionManager.clearSession();
        window.location.reload();
      }
    }, 60000); // Check every minute
    
    return () => clearInterval(interval);
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="business" element={<BusinessProfile />} />
            <Route path="financial-data" element={<FinancialData />} />
            <Route path="assessment" element={<Assessment />} />
            <Route path="assessment-list" element={<AssessmentList />} />
            <Route path="reports" element={<Reports />} />
          </Route>
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
