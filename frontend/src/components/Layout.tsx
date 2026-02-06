import React, { useState, useEffect } from 'react';
import { Outlet, Link } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Container,
  Chip
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Business as BusinessIcon,
  Assessment as AssessmentIcon,
  Description as ReportIcon,
  CloudUpload as UploadIcon,
  Timer as TimerIcon
} from '@mui/icons-material';
import { SessionManager } from '../utils/sessionManager';

const Layout: React.FC = () => {
  const [timeRemaining, setTimeRemaining] = useState(SessionManager.getTimeRemaining());

  useEffect(() => {
    // Update time remaining every minute
    const interval = setInterval(() => {
      setTimeRemaining(SessionManager.getTimeRemaining());
    }, 60000);

    return () => clearInterval(interval);
  }, []);

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 0, mr: 4 }}>
            Financial Health Assessment
          </Typography>
          
          <Box sx={{ flexGrow: 1, display: 'flex', gap: 1 }}>
            <Button
              color="inherit"
              component={Link}
              to="/dashboard"
              startIcon={<DashboardIcon />}
            >
              Dashboard
            </Button>
            <Button
              color="inherit"
              component={Link}
              to="/business"
              startIcon={<BusinessIcon />}
            >
              Business
            </Button>
            <Button
              color="inherit"
              component={Link}
              to="/financial-data"
              startIcon={<UploadIcon />}
            >
              Upload Data
            </Button>
            <Button
              color="inherit"
              component={Link}
              to="/assessment-list"
              startIcon={<AssessmentIcon />}
            >
              Assessments
            </Button>
            <Button
              color="inherit"
              component={Link}
              to="/reports"
              startIcon={<ReportIcon />}
            >
              Reports
            </Button>
          </Box>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Chip
              icon={<TimerIcon />}
              label={`Session: ${timeRemaining}m`}
              color="primary"
              variant="outlined"
              sx={{ color: 'white', borderColor: 'white' }}
            />
          </Box>
        </Toolbar>
      </AppBar>

      <Container component="main" sx={{ flexGrow: 1, py: 3 }}>
        <Outlet />
      </Container>

      <Box component="footer" sx={{ py: 3, px: 2, mt: 'auto', backgroundColor: '#f5f5f5' }}>
        <Container maxWidth="lg">
          <Typography variant="body2" color="text.secondary" align="center">
            © 2026 Financial Health Assessment Platform. All rights reserved.
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default Layout;
