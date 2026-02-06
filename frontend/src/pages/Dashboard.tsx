import { useEffect, useState } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Box,
  Button,
  CircularProgress,
  Alert
} from '@mui/material';
import {
  Assessment as AssessmentIcon,
  TrendingUp,
  AccountBalance,
  Warning
} from '@mui/icons-material';
import { SessionManager } from '../utils/sessionManager';

const Dashboard = () => {
  const [assessment, setAssessment] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Get session data
  const session = SessionManager.getSession();

  useEffect(() => {
    fetchLatestAssessment();
  }, []);

  const fetchLatestAssessment = async () => {
    const userId = session.userId;
    try {
      const response = await fetch(`http://localhost:8000/api/v1/assessment/latest/${userId}`);
      
      if (response.ok) {
        const data = await response.json();
        setAssessment(data.assessment);
      } else {
        // No assessment found - use defaults
        setAssessment(null);
      }
    } catch (err) {
      console.error('Failed to fetch assessment:', err);
      setAssessment(null);
    } finally {
      setLoading(false);
    }
  };

  // Format risk level for display
  const getRiskLevelDisplay = (riskLevel: string) => {
    const levels: any = {
      'low': { text: 'Low', color: '#4caf50' },
      'moderate': { text: 'Moderate', color: '#ff9800' },
      'high': { text: 'High', color: '#f44336' },
      'critical': { text: 'Critical', color: '#d32f2f' }
    };
    return levels[riskLevel] || { text: 'Unknown', color: '#757575' };
  };

  const cards = assessment ? [
    {
      title: 'Financial Health Score',
      value: `${Math.round(assessment.overall_health_score)}/100`,
      icon: <AssessmentIcon sx={{ fontSize: 40 }} />,
      color: assessment.overall_health_score >= 70 ? '#4caf50' : assessment.overall_health_score >= 50 ? '#ff9800' : '#f44336'
    },
    {
      title: 'Credit Rating',
      value: assessment.credit_rating || 'N/A',
      icon: <TrendingUp sx={{ fontSize: 40 }} />,
      color: '#2196f3'
    },
    {
      title: 'Liquidity Score',
      value: `${Math.round(assessment.liquidity_score)}/100`,
      icon: <AccountBalance sx={{ fontSize: 40 }} />,
      color: assessment.liquidity_score >= 70 ? '#4caf50' : '#ff9800'
    },
    {
      title: 'Risk Level',
      value: getRiskLevelDisplay(assessment.risk_level).text,
      icon: <Warning sx={{ fontSize: 40 }} />,
      color: getRiskLevelDisplay(assessment.risk_level).color
    }
  ] : [
    {
      title: 'Financial Health Score',
      value: '-',
      icon: <AssessmentIcon sx={{ fontSize: 40 }} />,
      color: '#757575'
    },
    {
      title: 'Credit Rating',
      value: '-',
      icon: <TrendingUp sx={{ fontSize: 40 }} />,
      color: '#757575'
    },
    {
      title: 'Liquidity Score',
      value: '-',
      icon: <AccountBalance sx={{ fontSize: 40 }} />,
      color: '#757575'
    },
    {
      title: 'Risk Level',
      value: '-',
      icon: <Warning sx={{ fontSize: 40 }} />,
      color: '#757575'
    }
  ];

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Financial Health Dashboard
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        AI-Powered Financial Analysis
      </Typography>
      {assessment && (
        <Alert severity="info" sx={{ mb: 3 }}>
          Showing latest assessment from {new Date(assessment.assessment_date).toLocaleDateString()} for {assessment.business_name || 'your business'}
        </Alert>
      )}

      {!assessment && (
        <Alert severity="info" sx={{ mb: 3 }}>
          No financial assessment available yet. Upload financial data to get started!
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Key Metrics Cards */}
        {cards.map((card, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography color="textSecondary" gutterBottom>
                      {card.title}
                    </Typography>
                    <Typography variant="h4" component="div">
                      {card.value}
                    </Typography>
                  </Box>
                  <Box sx={{ color: card.color }}>
                    {card.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}

        {/* Recent Activity */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Financial Activity
            </Typography>
            <Box sx={{ mt: 2 }}>
              {assessment ? (
                <>
                  <Typography variant="body2" color="text.secondary">
                    • Latest assessment completed: {new Date(assessment.assessment_date).toLocaleDateString()}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    • AI Model Used: {assessment.ai_model_used || 'Gemini 3 Flash'}
                  </Typography>
                  {assessment.strengths && assessment.strengths.length > 0 && (
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                      • {assessment.strengths.length} strengths identified
                    </Typography>
                  )}
                  {assessment.cost_optimization_recommendations && assessment.cost_optimization_recommendations.length > 0 && (
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                      • {assessment.cost_optimization_recommendations.length} recommendations available
                    </Typography>
                  )}
                </>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No recent activity. Upload financial data to get started.
                </Typography>
              )}
            </Box>
            <Button variant="contained" sx={{ mt: 3 }} href="/assessment-list">
              View Full Assessment
            </Button>
          </Paper>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Button variant="outlined" fullWidth href="/financial-data">
                Upload Financial Data
              </Button>
              <Button variant="outlined" fullWidth href="/assessment-list">
                View Assessments
              </Button>
              <Button variant="outlined" fullWidth href="/reports">
                Generate Report
              </Button>
              <Button variant="outlined" fullWidth href="/business">
                Business Profile
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* AI Insights */}
        {assessment && assessment.ai_summary && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3, bgcolor: 'primary.light', color: 'white' }}>
              <Typography variant="h6" gutterBottom>
                🤖 AI-Powered Insights
              </Typography>
              <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                {assessment.ai_summary.substring(0, 300)}...
              </Typography>
              {assessment.strengths && assessment.strengths.length > 0 && (
                <Box component="ul" sx={{ mt: 2 }}>
                  {assessment.strengths.slice(0, 3).map((strength: string, idx: number) => (
                    <li key={idx}>{strength}</li>
                  ))}
                </Box>
              )}
            </Paper>
          </Grid>
        )}
      </Grid>
    </Container>
  );
};

export default Dashboard;
