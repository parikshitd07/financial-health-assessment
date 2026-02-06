import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Container,
    Paper,
    Typography,
    Button,
    Box,
    Alert,
    LinearProgress,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Chip
} from '@mui/material';
import { CloudUpload, CheckCircle } from '@mui/icons-material';
import { SessionManager } from '../utils/sessionManager';

const FinancialData = () => {
    const navigate = useNavigate();
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [success, setSuccess] = useState('');
    const [error, setError] = useState('');
    
    // Get session data
    const session = SessionManager.getSession();

    const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0]) {
            const file = event.target.files[0];
            const validTypes = ['text/csv', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/pdf'];

            if (!validTypes.includes(file.type) && !file.name.match(/\.(csv|xlsx|xls|pdf)$/i)) {
                setError('Invalid file type. Please upload CSV, Excel, or PDF files only.');
                return;
            }

            if (file.size > 50 * 1024 * 1024) {
                setError('File size exceeds 50MB limit.');
                return;
            }

            setSelectedFile(file);
            setError('');
            setSuccess('');
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setError('Please select a file first.');
            return;
        }

        setUploading(true);
        setError('');
        setSuccess('');

        try {
            // Use session business ID
            const businessId = session.businessId;

            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('fiscal_year', '2024');
            formData.append('business_id', businessId.toString());

            const response = await fetch('http://localhost:8000/api/v1/financial-data/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Upload failed');
            }

            const result = await response.json();
            
            if (result.success) {
                const docType = result.document_type || 'financial document';
                setSuccess(
                    `✅ File "${selectedFile.name}" uploaded successfully!\n` +
                    `📊 Document Type: ${docType}\n` +
                    `🤖 AI Analysis: Complete!\n` +
                    `Redirecting to Assessment List...`
                );
                
                // Log parsed data for debugging
                console.log('Parsed Financial Data:', result.parsed_data);
                
                // Redirect to assessment list after 2 seconds
                setTimeout(() => {
                    navigate('/assessment-list');
                }, 2000);
            }
            
            setSelectedFile(null);

            // Reset file input
            const fileInput = document.getElementById('file-upload') as HTMLInputElement;
            if (fileInput) fileInput.value = '';

        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Upload failed';
            setError(`Upload failed: ${errorMessage}. Make sure the backend server is running.`);
            console.error('Upload error:', err);
        } finally {
            setUploading(false);
        }
    };

    // No hardcoded sample files - will show real uploaded files only
    const sampleFiles: any[] = [];

    return (
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Typography variant="h4" gutterBottom>
                Financial Data Management
            </Typography>
            <Typography variant="subtitle1" color="text.secondary" gutterBottom sx={{ mb: 4 }}>
                Upload your financial statements for AI-powered analysis
            </Typography>

            {/* Upload Section */}
            <Paper sx={{ p: 4, mb: 4 }}>
                <Typography variant="h6" gutterBottom>
                    Upload Financial Documents
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                    Supported formats: CSV, Excel (.xlsx), PDF (text-based) | Max size: 50MB
                </Typography>

                {error && (
                    <Alert severity="error" sx={{ mb: 2 }}>
                        {error}
                    </Alert>
                )}

                {success && (
                    <Alert severity="success" sx={{ mb: 2 }} icon={<CheckCircle />}>
                        {success}
                    </Alert>
                )}

                <Box sx={{ mb: 3 }}>
                    <input
                        accept=".csv,.xlsx,.xls,.pdf"
                        style={{ display: 'none' }}
                        id="file-upload"
                        type="file"
                        onChange={handleFileSelect}
                    />
                    <label htmlFor="file-upload">
                        <Button
                            variant="outlined"
                            component="span"
                            startIcon={<CloudUpload />}
                            size="large"
                        >
                            Choose File
                        </Button>
                    </label>

                    {selectedFile && (
                        <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
                            <Typography variant="body2">
                                <strong>Selected:</strong> {selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)
                            </Typography>
                        </Box>
                    )}
                </Box>

                <Button
                    variant="contained"
                    onClick={handleUpload}
                    disabled={!selectedFile || uploading}
                    size="large"
                    fullWidth
                    sx={{ mt: 2 }}
                >
                    {uploading ? 'Uploading...' : 'Upload and Analyze'}
                </Button>

                {uploading && <LinearProgress sx={{ mt: 2 }} />}
            </Paper>

            {/* Previously Uploaded Files */}
            <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                    Uploaded Financial Documents
                </Typography>

                <TableContainer>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell><strong>File Name</strong></TableCell>
                                <TableCell><strong>Type</strong></TableCell>
                                <TableCell><strong>Upload Date</strong></TableCell>
                                <TableCell><strong>Status</strong></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {sampleFiles.map((file, index) => (
                                <TableRow key={index}>
                                    <TableCell>{file.name}</TableCell>
                                    <TableCell>{file.type}</TableCell>
                                    <TableCell>{file.date}</TableCell>
                                    <TableCell>
                                        <Chip label={file.status} color="success" size="small" />
                                    </TableCell>
                                </TableRow>
                            ))}
                            {!sampleFiles.length && (
                                <TableRow>
                                    <TableCell colSpan={4} align="center">
                                        No files uploaded yet. Upload your first document above!
                                    </TableCell>
                                </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Paper>

            {/* Help Section */}
            <Paper sx={{ p: 3, mt: 4, bgcolor: 'grey.50' }}>
                <Typography variant="h6" gutterBottom>
                    💡 Need Help?
                </Typography>
                <Typography variant="body2">
                    See <strong>FINANCIAL_DOCUMENTS_GUIDE.md</strong> for:
                </Typography>
                <Box component="ul">
                    <li>What documents to upload</li>
                    <li>Sample CSV templates</li>
                    <li>File format requirements</li>
                    <li>Industry-specific guidance</li>
                </Box>
            </Paper>
        </Container>
    );
};

export default FinancialData;
