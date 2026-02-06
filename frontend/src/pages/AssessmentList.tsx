import { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Alert,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Grid,
  Card,
  CardContent,
  Divider,
  List,
  ListItem,
  ListItemText
} from '@mui/material';
import {
  Visibility,
  Assessment as AssessmentIcon,
  CheckCircle,
  Warning
} from '@mui/icons-material';
import { SessionManager } from '../utils/sessionManager';

interface AssessmentRecord {
  id: number;
  business_id: number;
  business_name: string;
  industry: string;
  assessment_date: string;
  overall_health_score: number;
  credit_rating: string;
  risk_level: string;
  liquidity_score: number;
  profitability_score: number;
  efficiency_score: number;
  ai_summary: string;
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  threats: string[];
  cost_optimization_recommendations: string[];
  revenue_enhancement_recommendations: string[];
  working_capital_recommendations: string[];
  tax_optimization_recommendations: string[];
  recommended_products: string[];
  ai_model_used: string;
}

const AssessmentList = () => {
  const [assessments, setAssessments] = useState<AssessmentRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedAssessment, setSelectedAssessment] = useState<AssessmentRecord | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  
  // Get session data
  const session = SessionManager.getSession();
  const currentUserId = session.userId;

  useEffect(() => {
    fetchAllAssessments();
  }, []);

  const fetchAllAssessments = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/assessment/user/${currentUserId}/all`);
      if (response.ok) {
        const data = await response.json();
        setAssessments(data.assessments || []);
      } else {
        setError('Failed to load assessments');
      }
    } catch (err) {
      console.error('Failed to fetch assessments:', err);
      setError('Failed to load assessments');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk: string) => {
    const colors: any = {
      'low': 'success',
      'moderate': 'warning',
      'high': 'error',
      'critical': 'error'
    };
    return colors[risk] || 'default';
  };

  const getScoreColor = (score: number) => {
    if (score >= 70) return 'success';
    if (score >= 50) return 'warning';
    return 'error';
  };

  const handleViewDetails = (assessment: AssessmentRecord) => {
    setSelectedAssessment(assessment);
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedAssessment(null);
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
        <AssessmentIcon sx={{ fontSize: 40, mr: 2, color: 'primary.main' }} />
        <Box>
          <Typography variant="h4" gutterBottom>
            All Assessment History
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Complete list of all financial assessments across all your businesses
          </Typography>
        </Box>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Assessments
              </Typography>
              <Typography variant="h3" color="primary">
                {assessments.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Average Health Score
              </Typography>
              <Typography variant="h3" color="primary">
                {assessments.length > 0 
                  ? Math.round(assessments.reduce((sum, a) => sum + a.overall_health_score, 0) / assessments.length)
                  : 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Latest Assessment
              </Typography>
              <Typography variant="h6" color="primary">
                {assessments.length > 0 
                  ? new Date(assessments[0].assessment_date).toLocaleDateString()
                  : 'N/A'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {assessments.length === 0 ? (
        <Alert severity="info">
          No assessments found. Upload financial data to generate your first assessment.
        </Alert>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow sx={{ bgcolor: 'primary.light' }}>
                <TableCell><strong>Date</strong></TableCell>
                <TableCell><strong>Business</strong></TableCell>
                <TableCell><strong>Industry</strong></TableCell>
                <TableCell align="center"><strong>Health Score</strong></TableCell>
                <TableCell align="center"><strong>Credit Rating</strong></TableCell>
                <TableCell align="center"><strong>Risk Level</strong></TableCell>
                <TableCell align="center"><strong>Liquidity</strong></TableCell>
                <TableCell align="center"><strong>Profitability</strong></TableCell>
                <TableCell align="center"><strong>Actions</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {assessments.map((assessment) => (
                <TableRow key={assessment.id} hover>
                  <TableCell>
                    {new Date(assessment.assessment_date).toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" fontWeight="bold">
                      {assessment.business_name}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" sx={{ textTransform: 'capitalize' }}>
                      {assessment.industry}
                    </Typography>
                  </TableCell>
                  <TableCell align="center">
                    <Chip 
                      label={Math.round(assessment.overall_health_score)}
                      color={getScoreColor(assessment.overall_health_score)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="center">
                    <Typography variant="h6" color="primary">
                      {assessment.credit_rating}
                    </Typography>
                  </TableCell>
                  <TableCell align="center">
                    <Chip 
                      label={assessment.risk_level.toUpperCase()}
                      color={getRiskColor(assessment.risk_level)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="center">
                    {Math.round(assessment.liquidity_score)}
                  </TableCell>
                  <TableCell align="center">
                    {Math.round(assessment.profitability_score)}
                  </TableCell>
                  <TableCell align="center">
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<Visibility />}
                      onClick={() => handleViewDetails(assessment)}
                    >
                      View
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Detailed View Dialog */}
      <Dialog 
        open={dialogOpen} 
        onClose={handleCloseDialog}
        maxWidth="lg"
        fullWidth
      >
        {selectedAssessment && (
          <>
            <DialogTitle>
              <Box>
                <Typography variant="h5">
                  Assessment Details - {selectedAssessment.business_name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {selectedAssessment.industry} • {new Date(selectedAssessment.assessment_date).toLocaleDateString()}
                </Typography>
              </Box>
            </DialogTitle>
            <DialogContent dividers>
              {/* Key Metrics */}
              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={6} md={3}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography color="textSecondary" variant="caption">
                        Health Score
                      </Typography>
                      <Typography variant="h4" color="primary">
                        {Math.round(selectedAssessment.overall_health_score)}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography color="textSecondary" variant="caption">
                        Credit Rating
                      </Typography>
                      <Typography variant="h4" color="primary">
                        {selectedAssessment.credit_rating}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography color="textSecondary" variant="caption">
                        Liquidity
                      </Typography>
                      <Typography variant="h4">
                        {Math.round(selectedAssessment.liquidity_score)}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography color="textSecondary" variant="caption">
                        Profitability
                      </Typography>
                      <Typography variant="h4">
                        {Math.round(selectedAssessment.profitability_score)}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>

              {/* AI Summary */}
              <Paper sx={{ p: 2, mb: 3, bgcolor: 'primary.light', color: 'white' }}>
                <Typography variant="h6" gutterBottom>
                  🤖 AI Analysis Summary
                </Typography>
                <Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>
                  {selectedAssessment.ai_summary}
                </Typography>
                <Typography variant="caption" sx={{ mt: 1, display: 'block', opacity: 0.9 }}>
                  Model: {selectedAssessment.ai_model_used}
                </Typography>
              </Paper>

              {/* SWOT */}
              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2 }} variant="outlined">
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <CheckCircle sx={{ color: 'success.main', mr: 1 }} />
                      <Typography variant="h6">Strengths</Typography>
                    </Box>
                    <List dense>
                      {selectedAssessment.strengths?.slice(0, 3).map((item, idx) => (
                        <ListItem key={idx}>
                          <ListItemText primary={`• ${item}`} />
                        </ListItem>
                      ))}
                    </List>
                  </Paper>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2 }} variant="outlined">
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <Warning sx={{ color: 'warning.main', mr: 1 }} />
                      <Typography variant="h6">Weaknesses</Typography>
                    </Box>
                    <List dense>
                      {selectedAssessment.weaknesses?.slice(0, 3).map((item, idx) => (
                        <ListItem key={idx}>
                          <ListItemText primary={`• ${item}`} />
                        </ListItem>
                      ))}
                    </List>
                  </Paper>
                </Grid>
              </Grid>

              {/* Recommendations Summary */}
              <Paper sx={{ p: 2 }} variant="outlined">
                <Typography variant="h6" gutterBottom>
                  💡 Key Recommendations
                </Typography>
                <Divider sx={{ mb: 2 }} />
                {selectedAssessment.cost_optimization_recommendations?.length > 0 && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="primary">
                      Cost Optimization ({selectedAssessment.cost_optimization_recommendations.length})
                    </Typography>
                    {selectedAssessment.cost_optimization_recommendations.slice(0, 2).map((item: any, idx: number) => {
                      const rec = typeof item === 'string' ? item : item.recommendation || '';
                      const area = typeof item === 'object' ? item.area : '';
                      return (
                        <Box key={idx} sx={{ mb: 1 }}>
                          {area && <Typography variant="caption" color="text.secondary">{area}</Typography>}
                          <Typography variant="body2">• {rec}</Typography>
                        </Box>
                      );
                    })}
                  </Box>
                )}
                {selectedAssessment.revenue_enhancement_recommendations?.length > 0 && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="primary">
                      Revenue Enhancement ({selectedAssessment.revenue_enhancement_recommendations.length})
                    </Typography>
                    {selectedAssessment.revenue_enhancement_recommendations.slice(0, 2).map((item: any, idx: number) => {
                      const rec = typeof item === 'string' ? item : item.recommendation || '';
                      const strategy = typeof item === 'object' ? item.strategy : '';
                      return (
                        <Box key={idx} sx={{ mb: 1 }}>
                          {strategy && <Typography variant="caption" color="text.secondary">{strategy}</Typography>}
                          <Typography variant="body2">• {rec}</Typography>
                        </Box>
                      );
                    })}
                  </Box>
                )}
                {selectedAssessment.tax_optimization_recommendations?.length > 0 && (
                  <Box>
                    <Typography variant="subtitle2" color="primary">
                      Tax Optimization ({selectedAssessment.tax_optimization_recommendations.length})
                    </Typography>
                    {selectedAssessment.tax_optimization_recommendations.slice(0, 2).map((item: any, idx: number) => {
                      const rec = typeof item === 'string' ? item : item.recommendation || '';
                      const area = typeof item === 'object' ? item.area : '';
                      return (
                        <Box key={idx} sx={{ mb: 1 }}>
                          {area && <Typography variant="caption" color="text.secondary">{area}</Typography>}
                          <Typography variant="body2">• {rec}</Typography>
                        </Box>
                      );
                    })}
                  </Box>
                )}
              </Paper>
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseDialog}>Close</Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Container>
  );
};

export default AssessmentList;
