# Functional Test Cases for Cloud Risk Assessment Agent

## Environment Setup Test Cases

| TC_ID | Title | Test Step Description | Expected Result |
|-------|--------|---------------------|-----------------|
| ENV_001 | Repository Setup | 1. Clone the repository from GitHub<br>2. Navigate to the cloned directory | Repository is cloned successfully without errors |
| ENV_002 | Environment File Configuration | 1. Create `.env` file in root directory<br>2. Add OpenAI API credentials<br>3. Add AWS credentials (if needed)<br>4. Save the file | `.env` file is created with all required credentials |
| ENV_003 | Docker Container Build | 1. Run `make run` command<br>2. Wait for container build process | Docker containers build successfully without errors |
| ENV_004 | Service Accessibility | 1. Wait for service startup<br>2. Access http://localhost<br>3. Verify login page | Service is accessible and login page is displayed |

## Configuration Test Cases

| TC_ID | Title | Test Step Description | Expected Result |
|-------|--------|---------------------|-----------------|
| CONF_001 | Basic Config Generation | 1. Run `make gen_config`<br>2. Select "n" for all scan options<br>3. Check generated config file | Config file is generated with empty scan settings |
| CONF_002 | Kubernetes Config | 1. Run `make gen_config`<br>2. Select "y" for Kubernetes scan<br>3. Provide kubeconfig path<br>4. Check config file | Config includes Kubernetes settings with correct path |
| CONF_003 | Code Scan Config | 1. Run `make gen_config`<br>2. Select "y" for code scan<br>3. Provide repository path<br>4. Check config file | Config includes code scan settings with correct path |
| CONF_004 | Container Scan Config | 1. Run `make gen_config`<br>2. Select "y" for container scan<br>3. Provide image tar path<br>4. Check config file | Config includes container scan settings with correct path |
| CONF_005 | AWS Scan Config | 1. Run `make gen_config`<br>2. Select "y" for AWS scan<br>3. Provide AWS region<br>4. Check config file | Config includes AWS settings with correct region |

## Scanning Test Cases

| TC_ID | Title | Test Step Description | Expected Result |
|-------|--------|---------------------|-----------------|
| SCAN_001 | Kubernetes Scan Execution | 1. Configure Kubernetes scan<br>2. Run `make scan`<br>3. Monitor scan progress<br>4. Check results in UI | Scan completes successfully with Kubernetes findings |
| SCAN_002 | Code Repository Scan | 1. Configure code scan<br>2. Run `make scan`<br>3. Monitor scan progress<br>4. Check results in UI | Code vulnerabilities are detected and reported |
| SCAN_003 | Container Image Scan | 1. Configure container scan<br>2. Run `make scan`<br>3. Monitor scan progress<br>4. Check results in UI | Container vulnerabilities are detected with CVE info |
| SCAN_004 | AWS Resources Scan | 1. Configure AWS scan<br>2. Run `make scan`<br>3. Monitor scan progress<br>4. Check results in UI | AWS misconfigurations are detected and reported |
| SCAN_005 | Multiple Resource Scan | 1. Configure all scan types<br>2. Run `make scan`<br>3. Monitor scan progress<br>4. Check results in UI | All configured scans complete successfully |

## Web Interface Test Cases

| TC_ID | Title | Test Step Description | Expected Result |
|-------|--------|---------------------|-----------------|
| WEB_001 | Basic Report Generation | 1. Access web interface<br>2. Enter `/report all`<br>3. Wait for response | Complete report is generated with all findings |
| WEB_002 | Filtered Report Generation | 1. Access web interface<br>2. Enter `/report kubernetes`<br>3. Wait for response | Report shows only Kubernetes findings |
| WEB_003 | High Severity Query | 1. Access web interface<br>2. Enter "Show high severity issues"<br>3. Wait for response | Only high severity findings are displayed |
| WEB_004 | CVSS Score Filter | 1. Access web interface<br>2. Enter "Show vulnerabilities with CVSS > 7"<br>3. Wait for response | Only findings with CVSS > 7 are shown |
| WEB_005 | Resource-Specific Query | 1. Access web interface<br>2. Enter "List AWS misconfigurations"<br>3. Wait for response | Only AWS misconfigurations are displayed |

## Additional Web Interface Test Cases

| TC_ID | Title | Test Step Description | Expected Result |
|-------|--------|---------------------|-----------------|
| WEB_006 | Chat History Persistence | 1. Submit multiple queries<br>2. Close browser<br>3. Reopen application<br>4. Check chat history | Previous chat history is preserved |
| WEB_007 | Message Formatting | 1. Generate report with different severity levels<br>2. Check formatting of messages<br>3. Verify code snippets display | Messages are properly formatted with correct colors and code highlighting |
| WEB_008 | Response Time Indicators | 1. Submit a long-running query<br>2. Observe loading indicators<br>3. Wait for response | Loading indicators show progress during processing |
| WEB_009 | Error Message Display | 1. Submit invalid query<br>2. Check error message display<br>3. Verify error formatting | Error messages are clear and properly formatted |
| WEB_010 | Navigation Controls | 1. Generate multiple reports<br>2. Use chat history navigation<br>3. Test scroll functionality | Navigation controls work smoothly |

## Database Management Test Cases

| TC_ID | Title | Test Step Description | Expected Result |
|-------|--------|---------------------|-----------------|
| DB_001 | Database Refresh | 1. Run `make refresh`<br>2. Confirm refresh prompt<br>3. Check database state | Database is cleared while maintaining schema |
| DB_002 | Sample Data Import | 1. Run `make sample`<br>2. Wait for import<br>3. Check web interface | Sample data is successfully imported |
| DB_003 | Database Backup | 1. Stop service<br>2. Copy database file<br>3. Restart service | Database is successfully backed up |
| DB_004 | Database Recovery | 1. Stop service<br>2. Restore database backup<br>3. Restart service | Database is successfully restored |

## Error Handling Test Cases

| TC_ID | Title | Test Step Description | Expected Result |
|-------|--------|---------------------|-----------------|
| ERR_001 | Invalid Kubeconfig | 1. Configure scan with invalid kubeconfig<br>2. Run scan<br>3. Check error handling | Clear error message about invalid kubeconfig |
| ERR_002 | Missing Repository | 1. Configure scan with non-existent repo<br>2. Run scan<br>3. Check error handling | Clear error message about missing repository |
| ERR_003 | Corrupted Image | 1. Configure scan with corrupted image<br>2. Run scan<br>3. Check error handling | Clear error message about corrupted image |
| ERR_004 | Invalid AWS Credentials | 1. Configure AWS scan with invalid credentials<br>2. Run scan<br>3. Check error handling | Clear error message about invalid credentials |

## Additional Scanning Test Cases

| TC_ID | Title | Test Step Description | Expected Result |
|-------|--------|---------------------|-----------------|
| SCAN_006 | Large Repository Scan | 1. Configure scan for large codebase<br>2. Run scan<br>3. Monitor memory usage<br>4. Check results | Large repository is scanned without memory issues |
| SCAN_007 | Multi-Container Scan | 1. Configure multiple container scans<br>2. Run scans sequentially<br>3. Check results | All containers are scanned successfully |
| SCAN_008 | Incremental Code Scan | 1. Scan repository<br>2. Make changes<br>3. Scan again<br>4. Compare results | Only changed files are rescanned |
| SCAN_009 | Custom Rule Scanning | 1. Add custom scanning rules<br>2. Run scan<br>3. Verify custom rule detection | Custom rules are properly applied |
| SCAN_010 | Scan Interruption Recovery | 1. Start scan<br>2. Interrupt process<br>3. Restart scan<br>4. Check recovery | Scan recovers from interruption gracefully |

## UI Component Test Cases

| TC_ID | Title | Test Step Description | Expected Result |
|-------|--------|---------------------|-----------------|
| UI_001 | Responsive Layout | 1. Access interface on desktop<br>2. Access on tablet<br>3. Access on mobile<br>4. Check layout | UI adapts correctly to different screen sizes |
| UI_002 | Theme Switching | 1. Switch to dark theme<br>2. Check all components<br>3. Switch to light theme<br>4. Verify colors | Themes apply correctly to all components |
| UI_003 | Accessibility Features | 1. Test keyboard navigation<br>2. Check screen reader compatibility<br>3. Verify ARIA labels | Interface is accessible via keyboard and screen readers |
| UI_004 | Input Validation | 1. Enter various invalid inputs<br>2. Check validation messages<br>3. Test input limits | Input validation works correctly with clear messages |
| UI_005 | Modal Dialogs | 1. Trigger confirmation dialogs<br>2. Check overlay behavior<br>3. Test close actions | Modals display and function correctly |

## Integration Test Cases

| TC_ID | Title | Test Step Description | Expected Result |
|-------|--------|---------------------|-----------------|
| INT_001 | Third-Party API Integration | 1. Test OpenAI API connection<br>2. Verify AWS SDK integration<br>3. Check Kubernetes client | All third-party integrations function correctly |
| INT_002 | Database Transactions | 1. Perform concurrent database operations<br>2. Check transaction isolation<br>3. Verify data consistency | Database maintains consistency under load |
| INT_003 | File System Integration | 1. Test file reading/writing<br>2. Check file permissions<br>3. Verify cleanup | File system operations work correctly |
| INT_004 | Docker Integration | 1. Test container operations<br>2. Verify volume mounts<br>3. Check network connectivity | Docker integration functions properly |
| INT_005 | Authentication Flow | 1. Test login process<br>2. Verify token handling<br>3. Check session management | Authentication flow works end-to-end |

## Compliance Test Cases

| TC_ID | Title | Test Step Description | Expected Result |
|-------|--------|---------------------|-----------------|
| COMP_001 | Data Privacy | 1. Check sensitive data handling<br>2. Verify data encryption<br>3. Test data retention | Compliance with data privacy requirements |
| COMP_002 | Audit Logging | 1. Perform various operations<br>2. Check audit logs<br>3. Verify log format | All required actions are properly logged |
| COMP_003 | Access Control | 1. Test different user roles<br>2. Verify permission enforcement<br>3. Check audit trail | Access control policies are enforced |
| COMP_004 | Data Retention | 1. Create old records<br>2. Wait for retention period<br>3. Verify cleanup | Data retention policies are followed |
| COMP_005 | Regulatory Compliance | 1. Check security controls<br>2. Verify compliance reports<br>3. Test export functions | Meets regulatory requirements |

## Performance Test Cases

| TC_ID | Title | Test Step Description | Expected Result |
|-------|--------|---------------------|-----------------|
| PERF_001 | Concurrent Scans | 1. Configure multiple scans<br>2. Run scans simultaneously<br>3. Monitor system performance | All scans complete without interference |
| PERF_002 | Multiple Reports | 1. Generate multiple reports<br>2. Request reports concurrently<br>3. Monitor response times | Reports generate without significant delay |
| PERF_003 | Database Performance | 1. Import large dataset<br>2. Run complex queries<br>3. Monitor query response time | Queries complete within acceptable time |
| PERF_004 | System Load | 1. Run full scan suite<br>2. Generate reports<br>3. Monitor system resources | System remains responsive under load |
| PERF_005 | Memory Usage | 1. Monitor memory during scans<br>2. Check for memory leaks<br>3. Test with large datasets | Memory usage remains within limits |
| PERF_006 | CPU Utilization | 1. Monitor CPU during operations<br>2. Test parallel processing<br>3. Check resource limits | CPU usage is optimized |
| PERF_007 | Network Performance | 1. Test with limited bandwidth<br>2. Check large file transfers<br>3. Monitor timeouts | Network operations handle constraints |
| PERF_008 | Database Scaling | 1. Test with large result sets<br>2. Check query performance<br>3. Monitor connection pool | Database performs well at scale |
| PERF_009 | Concurrent Users | 1. Simulate multiple users<br>2. Test concurrent operations<br>3. Monitor response times | System handles concurrent users effectively |

## Notes for Test Execution
1. Prerequisites:
   - Clean test environment
   - Required credentials and access
   - Test data sets
2. Test Environment Setup:
   - Docker installed and configured
   - Required ports available
   - Sufficient disk space
3. Test Data Management:
   - Use version-controlled test data
   - Clean up after tests
   - Document test data dependencies
4. Monitoring Requirements:
   - CPU and memory usage
   - Network traffic
   - Error logs
   - Performance metrics 