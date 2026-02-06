import { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper,
  Grid,
  Card,
  CardContent,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Alert,
  SelectChangeEvent
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Assessment as AssessmentIcon,
  Warning,
  CheckCircle
} from '@mui/icons-material';

interface Business {
  id: number;
  business_name: string;
  industry: string;
  city: string;
  state: string;
}

interface Assessment {
  id: number;
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

const AssessmentPage: React.FC = () => {
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [selectedBusinessId, setSelectedBusinessId] = useState<string>('');
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [selectedAssessment, setSelectedAssessment] = useState<Assessment | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // For demo, using user_id = 1 (you can get this from auth context)
  const currentUserId = 1;

  useEffect(() => {
    fetchUserBusinesses();
  }, []);

  useEffect(() => {
    if (selectedBusinessId) {
      fetchAssessments(parseInt(selectedBusinessId));
    }
  }, [selectedBusinessId]);

  const fetchUserBusinesses = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/business/user/${currentUserId}`);
      if (response.ok) {
        const data = await response.json();
        setBusinesses(data);
        
        // Auto-select first business if available
        if (data.length > 0) {
          setSelectedBusinessId(data[0].id.toString());
        }
      }
    } catch (err) {
      console.error('Failed to fetch businesses:', err);
      setError('Failed to load businesses');
    } finally {
      setLoading(false);
    }
  };

  const fetchAssessments = async (businessId: number) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/v1/assessment/business/${businessId}`);
      if (response.ok) {
        const data = await response.json();
        setAssessments(data.assessments || []);
        
        // Auto-select latest assessment
        if (data.assessments && data.assessments.length > 0) {
          setSelectedAssessment(data.assessments[0]);
        } else {
          setSelectedAssessment(null);
        }
      } else {
        setAssessments([]);
        setSelectedAssessment(null);
      }
    } catch (err) {
      console.error('Failed to fetch assessments:', err);
      setError('Failed to load assessments');
    } finally {
      setLoading(false);
    }
  };

  const handleBusinessChange = (event: SelectChangeEvent) => {
    setSelectedBusinessId(event.target.value);
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
    if (score >= 70) return '#4caf50';
    if (score >= 50) return '#ff9800';
    return '#f44336';
  };

  if (loading && businesses.length === 0) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Financial Assessment History
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        View comprehensive AI-powered financial analysis for your businesses
      </Typography>

      {/* Company Selector */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <FormControl fullWidth>
          <InputLabel>Select Company</InputLabel>
          <Select
            value={selectedBusinessId}
            label="Select Company"
            onChange={handleBusinessChange}
          >
            {businesses.map((business) => (
              <MenuItem key={business.id} value={business.id.toString()}>
                <Box>
                  <Typography variant="body1">{business.business_name}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    {business.industry} • {business.city}, {business.state}
                  </Typography>
                </Box>
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        
        {businesses.length === 0 && (
          <Alert severity="info" sx={{ mt: 2 }}>
            No businesses found. Please create a business profile first.
          </Alert>
        )}
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Assessment Results */}
      {selectedBusinessId && assessments.length === 0 && !loading && (
        <Alert severity="info">
          No assessments available for this business. Upload financial data to generate an assessment.
        </Alert>
      )}

      {selectedAssessment && (
        <>
          {/* Key Metrics */}
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Financial Health Score
                  </Typography>
                  <Typography variant="h3" sx={{ color: getScoreColor(selectedAssessment.overall_health_score) }}>
                    {Math.round(selectedAssessment.overall_health_score)}
                  </Typography>
                  <Typography variant="caption">out of 100</Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Credit Rating
                  </Typography>
                  <Typography variant="h3" color="primary">
                    {selectedAssessment.credit_rating}
                  </Typography>
                  <Chip 
                    label={selectedAssessment.risk_level.toUpperCase()} 
                    color={getRiskColor(selectedAssessment.risk_level)}
                    size="small"
                    sx={{ mt: 1 }}
                  />
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Liquidity Score
                  </Typography>
                  <Typography variant="h3" sx={{ color: getScoreColor(selectedAssessment.liquidity_score) }}>
                    {Math.round(selectedAssessment.liquidity_score)}
                  </Typography>
                  <Typography variant="caption">out of 100</Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Profitability Score
                  </Typography>
                  <Typography variant="h3" sx={{ color: getScoreColor(selectedAssessment.profitability_score) }}>
                    {Math.round(selectedAssessment.profitability_score)}
                  </Typography>
                  <Typography variant="caption">out of 100</Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* AI Summary */}
          <Paper sx={{ p: 3, mb: 3, bgcolor: 'primary.light', color: 'white' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <AssessmentIcon sx={{ mr: 1 }} />
              <Typography variant="h6">
                AI-Powered Analysis Summary
              </Typography>
            </Box>
            <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
              {selectedAssessment.ai_summary}
            </Typography>
            <Typography variant="caption" sx={{ mt: 2, display: 'block', opacity: 0.9 }}>
              Analyzed by: {selectedAssessment.ai_model_used} • 
              Date: {new Date(selectedAssessment.assessment_date).toLocaleDateString()}
            </Typography>
          </Paper>

          {/* SWOT Analysis */}
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, height: '100%' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <CheckCircle sx={{ color: 'success.main', mr: 1 }} />
                  <Typography variant="h6">Strengths</Typography>
                </Box>
                <List>
                  {selectedAssessment.strengths?.map((strength, idx) => (
                    <ListItem key={idx}>
                      <ListItemText primary={`• ${strength}`} />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>

            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, height: '100%' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Warning sx={{ color: 'warning.main', mr: 1 }} />
                  <Typography variant="h6">Weaknesses</Typography>
                </Box>
                <List>
                  {selectedAssessment.weaknesses?.map((weakness, idx) => (
                    <ListItem key={idx}>
                      <ListItemText primary={`• ${weakness}`} />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>

            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, height: '100%' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <TrendingUp sx={{ color: 'info.main', mr: 1 }} />
                  <Typography variant="h6">Opportunities</Typography>
                </Box>
                <List>
                  {selectedAssessment.opportunities?.map((opportunity, idx) => (
                    <ListItem key={idx}>
                      <ListItemText primary={`• ${opportunity}`} />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>

            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, height: '100%' }}>
                <Box sx={{ display: 'flex', alignments: 'center', mb: 2 }}>
                  <TrendingDown sx={{ color: 'error.main', mr: 1 }} />
                  <Typography variant="h6">Threats</Typography>
                </Box>
                <List>
                  {selectedAssessment.threats?.map((threat, idx) => (
                    <ListItem key={idx}>
                      <ListItemText primary={`• ${threat}`} />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>
          </Grid>

          {/* Recommendations */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              💡 Actionable Recommendations
            </Typography>
            <Divider sx={{ mb: 2 }} />

            {selectedAssessment.cost_optimization_recommendations?.length > 0 && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle1" color="primary" gutterBottom>
                  Cost Optimization
                </Typography>
                <List>
                  {selectedAssessment.cost_optimization_recommendations.map((rec, idx) => (
                    <ListItem key={idx}>
                      <ListItemText primary={`${idx + 1}. ${rec}`} />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}

            {selectedAssessment.revenue_enhancement_recommendations?.length > 0 && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle1" color="primary" gutterBottom>
                  Revenue Enhancement
                </Typography>
                <List>
                  {selectedAssessment.revenue_enhancement_recommendations.map((rec, idx) => (
                    <ListItem key={idx}>
                      <ListItemText primary={`${idx + 1}. ${rec}`} />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}

            {selectedAssessment.working_capital_recommendations?.length > 0 && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle1" color="primary" gutterBottom>
                  Working Capital Optimization
                </Typography>
                <List>
                  {selectedAssessment.working_capital_recommendations.map((rec, idx) => (
                    <ListItem key={idx}>
                      <ListItemText primary={`${idx + 1}. ${rec}`} />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}

            {selectedAssessment.tax_optimization_recommendations?.length > 0 && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle1" color="primary" gutterBottom>
                  Tax Optimization
                </Typography>
                <List>
                  {selectedAssessment.tax_optimization_recommendations.map((rec, idx) => (
                    <ListItem key={idx}>
                      <ListItemText primary={`${idx + 1}. ${rec}`} />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}

            {selectedAssessment.recommended_products?.length > 0 && (
              <Box>
                <Typography variant="subtitle1" color="primary" gutterBottom>
                  Recommended Financial Products
                </Typography>
                <List>
                  {selectedAssessment.recommended_products.map((product, idx) => (
                    <ListItem key={idx}>
                      <ListItemText primary={`${idx + 1}. ${product}`} />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}
          </Paper>

          {/* Assessment History */}
          {assessments.length > 1 && (
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Assessment History
              </Typography>
              <List>
                {assessments.map((assessment, idx) => (
                  <ListItem 
                    key={assessment.id}
                    button
                    selected={selectedAssessment.id === assessment.id}
                    onClick={() => setSelectedAssessment(assessment)}
                  >
                    <ListItemText
                      primary={`Assessment #${assessments.length - idx}`}
                      secondary={`${new Date(assessment.assessment_date).toLocaleDateString()} • Score: ${Math.round(assessment.overall_health_score)} • Rating: ${assessment.credit_rating}`}
                    />
                  </ListItem>
                ))}
              </List>
            </Paper>
          )}
        </>
      )}
    </Container>
  );
};

export default AssessmentPage;
