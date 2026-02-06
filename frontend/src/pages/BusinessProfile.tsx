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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  CircularProgress,
  Alert,
  Chip,
  IconButton
} from '@mui/material';
import {
  Business as BusinessIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon
} from '@mui/icons-material';
import { SessionManager } from '../utils/sessionManager';

interface Business {
  id: number;
  name: string;
  industry: string;
  registration_number: string;
  tax_id: string;
  address: string;
  phone: string;
  email: string;
  website: string;
  established_date: string;
  employee_count: number;
  annual_revenue: number;
  description: string;
}

const BusinessProfile = () => {
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingBusiness, setEditingBusiness] = useState<Business | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    industry: '',
    registration_number: '',
    tax_id: '',
    address: '',
    phone: '',
    email: '',
    website: '',
    established_date: '',
    employee_count: 0,
    annual_revenue: 0,
    description: ''
  });

  // Get session data
  const session = SessionManager.getSession();
  const currentUserId = session.userId;

  useEffect(() => {
    fetchBusinesses();
  }, []);

  const fetchBusinesses = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/business/user/${currentUserId}`);
      if (response.ok) {
        const data = await response.json();
        setBusinesses(data.businesses || []);
      } else {
        setError('Failed to load businesses');
      }
    } catch (err) {
      console.error('Failed to fetch businesses:', err);
      setError('Failed to load businesses');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (business?: Business) => {
    if (business) {
      setEditingBusiness(business);
      setFormData({
        name: business.name,
        industry: business.industry,
        registration_number: business.registration_number || '',
        tax_id: business.tax_id || '',
        address: business.address || '',
        phone: business.phone || '',
        email: business.email || '',
        website: business.website || '',
        established_date: business.established_date || '',
        employee_count: business.employee_count || 0,
        annual_revenue: business.annual_revenue || 0,
        description: business.description || ''
      });
    } else {
      setEditingBusiness(null);
      setFormData({
        name: '',
        industry: '',
        registration_number: '',
        tax_id: '',
        address: '',
        phone: '',
        email: '',
        website: '',
        established_date: '',
        employee_count: 0,
        annual_revenue: 0,
        description: ''
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingBusiness(null);
    setError('');
    setSuccess('');
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'employee_count' || name === 'annual_revenue' ? Number(value) : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const url = editingBusiness
        ? `http://localhost:8000/api/v1/business/${editingBusiness.id}`
        : 'http://localhost:8000/api/v1/business/';
      
      const method = editingBusiness ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          user_id: currentUserId
        }),
      });

      if (response.ok) {
        setSuccess(editingBusiness ? 'Business updated successfully!' : 'Business created successfully!');
        fetchBusinesses();
        setTimeout(() => {
          handleCloseDialog();
        }, 1500);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to save business');
      }
    } catch (err) {
      setError('Failed to save business');
    }
  };

  const handleDelete = async (businessId: number) => {
    if (!window.confirm('Are you sure you want to delete this business?')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/v1/business/${businessId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setSuccess('Business deleted successfully!');
        fetchBusinesses();
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError('Failed to delete business');
      }
    } catch (err) {
      setError('Failed to delete business');
    }
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
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <BusinessIcon sx={{ fontSize: 40, mr: 2, color: 'primary.main' }} />
          <Box>
            <Typography variant="h4" gutterBottom>
              My Businesses
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Manage your business profiles
            </Typography>
          </Box>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Add Business
        </Button>
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

      {businesses.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <BusinessIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No businesses yet
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Add your first business to get started with financial assessments
          </Typography>
          <Button variant="contained" startIcon={<AddIcon />} onClick={() => handleOpenDialog()}>
            Add Your First Business
          </Button>
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {businesses.map((business) => (
            <Grid item xs={12} md={6} key={business.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                    <Box>
                      <Typography variant="h5" gutterBottom>
                        {business.name}
                      </Typography>
                      <Chip label={business.industry} size="small" color="primary" />
                    </Box>
                    <Box>
                      <IconButton size="small" onClick={() => handleOpenDialog(business)}>
                        <EditIcon />
                      </IconButton>
                      <IconButton size="small" color="error" onClick={() => handleDelete(business.id)}>
                        <DeleteIcon />
                      </IconButton>
                    </Box>
                  </Box>

                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {business.description || 'No description provided'}
                  </Typography>

                  <Grid container spacing={2}>
                    {business.registration_number && (
                      <Grid item xs={12}>
                        <Typography variant="caption" color="text.secondary">
                          Registration: {business.registration_number}
                        </Typography>
                      </Grid>
                    )}
                    {business.email && (
                      <Grid item xs={12}>
                        <Typography variant="caption" color="text.secondary">
                          Email: {business.email}
                        </Typography>
                      </Grid>
                    )}
                    {business.phone && (
                      <Grid item xs={12}>
                        <Typography variant="caption" color="text.secondary">
                          Phone: {business.phone}
                        </Typography>
                      </Grid>
                    )}
                    {business.employee_count > 0 && (
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          Employees: {business.employee_count}
                        </Typography>
                      </Grid>
                    )}
                    {business.annual_revenue > 0 && (
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          Revenue: ${business.annual_revenue.toLocaleString()}
                        </Typography>
                      </Grid>
                    )}
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Add/Edit Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingBusiness ? 'Edit Business' : 'Add New Business'}
        </DialogTitle>
        <DialogContent>
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  label="Business Name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  label="Industry"
                  name="industry"
                  value={formData.industry}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Registration Number"
                  name="registration_number"
                  value={formData.registration_number}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Tax ID"
                  name="tax_id"
                  value={formData.tax_id}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Address"
                  name="address"
                  value={formData.address}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Website"
                  name="website"
                  value={formData.website}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Established Date"
                  name="established_date"
                  type="date"
                  value={formData.established_date}
                  onChange={handleChange}
                  InputLabelProps={{ shrink: true }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Employee Count"
                  name="employee_count"
                  type="number"
                  value={formData.employee_count}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Annual Revenue"
                  name="annual_revenue"
                  type="number"
                  value={formData.annual_revenue}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Description"
                  name="description"
                  multiline
                  rows={3}
                  value={formData.description}
                  onChange={handleChange}
                />
              </Grid>
            </Grid>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingBusiness ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default BusinessProfile;
