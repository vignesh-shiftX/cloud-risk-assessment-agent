# Manual Test Cases for Cloud Risk Assessment Agent

## Environment Setup Tests

### Test Case 1: Initial Setup
**Objective**: Verify that the application can be set up correctly
1. Clone the repository
2. Create `.env` file with required credentials
3. Run `make run`
**Expected Results**:
- Repository clones successfully
- Docker containers build without errors
- Service starts and is accessible at http://localhost

### Test Case 2: Configuration Generation
**Objective**: Verify scan configuration generation
1. Run `make gen_config`
2. Follow the interactive prompts for each scan type
3. Check the generated configuration file
**Expected Results**:
- Interactive prompts work correctly
- Configuration file is generated at `/tmp/tmcybertron/agent.yaml`
- Configuration file contains all selected options

## Scanning Tests

### Test Case 3: Kubernetes Scanning
**Objective**: Verify Kubernetes cluster scanning functionality
**Prerequisites**: Valid kubeconfig file
1. Copy kubeconfig to `/tmp/tmcybertron/.kube/config`
2. Configure Kubernetes scanning via `make gen_config`
3. Run `make scan`
4. Check results in the web interface
**Expected Results**:
- Scan completes without errors
- Results are stored in the database
- Findings are visible in the web interface
- Security issues are properly categorized

### Test Case 4: Code Repository Scanning
**Objective**: Verify code repository scanning functionality
1. Clone a test repository to `/tmp/tmcybertron/repo/`
2. Configure code scanning via `make gen_config`
3. Run `make scan`
4. Check results in the web interface
**Expected Results**:
- Code is scanned successfully
- Vulnerabilities are detected and reported
- Results show proper file locations and line numbers

### Test Case 5: Container Image Scanning
**Objective**: Verify container image scanning functionality
1. Save a test Docker image using `docker save -o /tmp/tmcybertron/image_file/test.tar image:tag`
2. Configure container scanning via `make gen_config`
3. Run `make scan`
4. Check results in the web interface
**Expected Results**:
- Container vulnerabilities are detected
- CVE information is properly displayed
- Severity levels are correctly assigned

### Test Case 6: AWS Resource Scanning
**Objective**: Verify AWS resource scanning functionality
**Prerequisites**: Valid AWS credentials in .env file
1. Configure AWS scanning via `make gen_config`
2. Run `make scan`
3. Check results in the web interface
**Expected Results**:
- AWS resources are scanned successfully
- Misconfigurations are detected
- Results are properly categorized by service

## Web Interface Tests

### Test Case 7: Report Generation
**Objective**: Verify report generation functionality
1. Access the web interface
2. Use the `/report` command with different options:
   - `/report all`
   - `/report kubernetes`
   - `/report aws`
   - `/report code`
   - `/report container`
3. Check the generated reports
**Expected Results**:
- Reports are generated for each category
- Reports contain accurate information
- Formatting is consistent
- All severity levels are properly color-coded

### Test Case 8: Query Functionality
**Objective**: Verify natural language query functionality
1. Try various queries:
   - "Show me all high severity issues"
   - "What are the kubernetes vulnerabilities?"
   - "List AWS misconfigurations"
   - "Show container vulnerabilities with CVSS score > 7"
2. Check the responses
**Expected Results**:
- Queries return relevant results
- Results are properly formatted
- Response times are reasonable
- Filtering works correctly

### Test Case 9: Database Management
**Objective**: Verify database management functions
1. Run `make refresh` to clear the database
2. Run `make sample` to load sample data
3. Check the results in the web interface
**Expected Results**:
- Database is cleared successfully
- Sample data is loaded correctly
- Web interface reflects the changes
- No errors during operations

## Error Handling Tests

### Test Case 10: Invalid Configuration Handling
**Objective**: Verify error handling for invalid configurations
1. Create invalid configurations:
   - Invalid kubeconfig file
   - Non-existent code repository
   - Corrupted container image
   - Invalid AWS credentials
2. Attempt to run scans
**Expected Results**:
- Clear error messages are displayed
- Application doesn't crash
- Proper error logging
- User is notified of the specific issue

### Test Case 11: Recovery Tests
**Objective**: Verify system recovery capabilities
1. Stop the service during a scan
2. Restart the service
3. Check the database integrity
4. Verify incomplete scans are handled properly
**Expected Results**:
- Service recovers gracefully
- Database remains consistent
- Incomplete scans are properly marked
- User is notified of the interruption

## Performance Tests

### Test Case 12: Load Testing
**Objective**: Verify system performance under load
1. Run multiple scans simultaneously
2. Generate multiple reports concurrently
3. Submit multiple queries in quick succession
**Expected Results**:
- System remains responsive
- Scans complete successfully
- No database locks or conflicts
- Response times remain reasonable

## Security Tests

### Test Case 13: Access Control
**Objective**: Verify security controls
1. Attempt to access the system without authentication
2. Try to access the database directly
3. Check for exposed sensitive information in logs
**Expected Results**:
- Unauthorized access is blocked
- Database is properly secured
- No sensitive information in logs
- All communications are encrypted

## Notes for QA Team
1. Document any bugs found with:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Screenshots/logs
2. Pay special attention to:
   - Error messages clarity
   - System stability
   - Data accuracy
   - Performance under load
3. Test on different:
   - Operating systems
   - Browser versions
   - Network conditions 