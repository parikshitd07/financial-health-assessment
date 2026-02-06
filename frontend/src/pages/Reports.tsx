import { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  Box,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip
} from '@mui/material';
import {
  Description as ReportIcon,
  Download as DownloadIcon,
  PictureAsPdf as PdfIcon,
  Assessment as AssessmentIcon
} from '@mui/icons-material';
import { SessionManager } from '../utils/sessionManager';

interface Business {
  id: number;
  name: string;
  industry: string;
}

interface Assessment {
  id: number;
  business_id: number;
  business_name: string;
  assessment_date: string;
  overall_health_score: number;
  credit_rating: string;
  risk_level: string;
}

const Reports = () => {
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [selectedBusiness, setSelectedBusiness] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Get session data
  const session = SessionManager.getSession();
  const currentUserId = session.userId;

  useEffect(() => {
    fetchBusinesses();
    fetchAllAssessments();
  }, []);

  useEffect(() => {
    if (selectedBusiness > 0) {
      fetchBusinessAssessments(selectedBusiness);
    }
  }, [selectedBusiness]);

  const fetchBusinesses = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/business/user/${currentUserId}`);
      if (response.ok) {
        const data = await response.json();
        setBusinesses(data.businesses || []);
      }
    } catch (err) {
      console.error('Failed to fetch businesses:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAllAssessments = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/assessment/user/${currentUserId}/all`);
      if (response.ok) {
        const data = await response.json();
        setAssessments(data.assessments || []);
      }
    } catch (err) {
      console.error('Failed to fetch assessments:', err);
    }
  };

  const fetchBusinessAssessments = async (businessId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/assessment/business/${businessId}`);
      if (response.ok) {
        const data = await response.json();
        setAssessments(data.assessments || []);
      }
    } catch (err) {
      console.error('Failed to fetch business assessments:', err);
    }
  };

  const handleGenerateReport = async (assessmentId: number, format: string) => {
    setGenerating(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/reports/assessment/${assessmentId}?format=${format}`,
        {
          method: 'GET',
        }
      );

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        // Set proper file extension based on format
        let extension = format;
        if (format === 'pdf') {
          extension = 'txt';  // Backend returns text file
        } else if (format === 'excel') {
          extension = 'xlsx';  // Backend returns xlsx file
        }
        
        a.download = `financial_report_${assessmentId}.${extension}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        setSuccess(`Report generated successfully!`);
      } else {
        setError('Failed to generate report');
      }
    } catch (err) {
      setError('Failed to generate report');
    } finally {
      setGenerating(false);
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

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
        <ReportIcon sx={{ fontSize: 40, mr: 2, color: 'primary.main' }} />
        <Box>
          <Typography variant="h4" gutterBottom>
            Financial Reports
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Generate and download comprehensive financial assessment reports
          </Typography>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccess('')}>
          {success}
        </Alert>
      )}

      {/* Filters */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Filter Reports
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Select Business</InputLabel>
              <Select
                value={selectedBusiness}
                label="Select Business"
                onChange={(e) => setSelectedBusiness(Number(e.target.value))}
              >
                <MenuItem value={0}>All Businesses</MenuItem>
                {businesses.map((business) => (
                  <MenuItem key={business.id} value={business.id}>
                    {business.name} ({business.industry})
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Paper>

      {/* Report Generation Options */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <PdfIcon sx={{ fontSize: 40, color: 'error.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                PDF Report
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Comprehensive PDF report with all financial metrics, AI insights, and recommendations
              </Typography>
              <Chip label="Most Popular" color="primary" size="small" />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <AssessmentIcon sx={{ fontSize: 40, color: 'success.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Excel Report
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Detailed Excel spreadsheet with financial ratios, trends, and analysis data
              </Typography>
              <Chip label="Data Analysis" color="success" size="small" />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <ReportIcon sx={{ fontSize: 40, color: 'info.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Summary Report
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Quick summary report with key metrics and executive overview
              </Typography>
              <Chip label="Quick View" color="info" size="small" />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Available Reports */}
      <Typography variant="h5" gutterBottom sx={{ mt: 4, mb: 2 }}>
        Available Reports
      </Typography>

      {assessments.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <AssessmentIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No assessments available
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Upload financial data and generate assessments to create reports
          </Typography>
          <Button variant="contained" href="/financial-data">
            Upload Financial Data
          </Button>
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {assessments.map((assessment) => (
            <Grid item xs={12} key={assessment.id}>
              <Card>
                <CardContent>
                  <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} md={4}>
                      <Typography variant="h6">
                        {assessment.business_name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {new Date(assessment.assessment_date).toLocaleDateString()}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                        <Chip 
                          label={`Score: ${Math.round(assessment.overall_health_score)}`}
                          color="primary"
                          size="small"
                        />
                        <Chip 
                          label={`Rating: ${assessment.credit_rating}`}
                          color="info"
                          size="small"
                        />
                        <Chip 
                          label={`Risk: ${assessment.risk_level.toUpperCase()}`}
                          color={getRiskColor(assessment.risk_level)}
                          size="small"
                        />
                      </Box>
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end', flexWrap: 'wrap' }}>
                        <Button
                          variant="contained"
                          size="small"
                          startIcon={<DownloadIcon />}
                          onClick={() => handleGenerateReport(assessment.id, 'pdf')}
                          disabled={generating}
                        >
                          PDF
                        </Button>
                        <Button
                          variant="outlined"
                          size="small"
                          startIcon={<DownloadIcon />}
                          onClick={() => handleGenerateReport(assessment.id, 'excel')}
                          disabled={generating}
                        >
                          Excel
                        </Button>
                        <Button
                          variant="outlined"
                          size="small"
                          startIcon={<DownloadIcon />}
                          onClick={() => handleGenerateReport(assessment.id, 'json')}
                          disabled={generating}
                        >
                          JSON
                        </Button>
                      </Box>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {generating && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
          <CircularProgress />
          <Typography variant="body2" sx={{ ml: 2, mt: 1 }}>
            Generating report...
          </Typography>
        </Box>
      )}

      {/* Report Features */}
      <Paper sx={{ p: 3, mt: 4, bgcolor: 'primary.light', color: 'white' }}>
        <Typography variant="h6" gutterBottom>
          📊 Report Features
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Typography variant="body2">
              • Comprehensive financial analysis
            </Typography>
            <Typography variant="body2">
              • AI-powered insights and recommendations
            </Typography>
            <Typography variant="body2">
              • SWOT analysis
            </Typography>
          </Grid>
          <Grid item xs={12} md={6}>
            <Typography variant="body2">
              • 30+ financial ratios
            </Typography>
            <Typography variant="body2">
              • Risk assessment and credit rating
            </Typography>
            <Typography variant="body2">
              • Actionable recommendations
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default Reports;
