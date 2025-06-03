| TC_ID | Category | Title | Test Step Description | Expected Result |
|-------|----------|-------|----------------------|-----------------|
| TC_UI_001 | Core Functionality | Send /report all Command | Open the Chainlit app, enter "/report all" in the chat input, and press Enter. | The chat displays a summary report response for all categories. |
| TC_UI_002 | Core Functionality | Send Natural Language Query | Open the Chainlit app, enter "Show me high severity vulnerabilities" in the chat input, and press Enter. | The chat displays a relevant response listing high severity vulnerabilities. |
| TC_UI_003 | Input Robustness & Error Handling | Invalid /report Command | Open the Chainlit app, enter "/report invalid" in the chat input, and press Enter. | The chat displays an error message indicating the report type is invalid. |
| TC_UI_004 | Input Robustness & Error Handling | Empty Input Submission | Open the Chainlit app, leave the chat input empty, and press Enter. | The chat displays a validation error or does not send a message. |
| TC_UI_005 | Core Functionality | Multiple Sequential Queries | Open the Chainlit app, send "/report aws" followed by "Give me a summary of container issues" in sequence. | The chat displays appropriate responses for each query in order. |
| TC_UI_006 | Core Functionality | CLI Command Input | Use the CLI to run `make scan` and check the output. | The CLI outputs scan progress and results without errors. |
| TC_UI_007 | UI Interactions | UI Button Interaction | Click the "Generate Executive Summary" button in the UI. | The summary section updates with the latest executive summary. |
| TC_UI_008 | Core Functionality | Summary Section Validation | After a scan, navigate to the summary section. | The summary section displays accurate and up-to-date scan results. |
| TC_UI_009 | Core Functionality | Security Report Correctness | Request a security report for a specific resource. | The report lists correct vulnerabilities and matches backend data. |
| TC_UI_010 | Core Functionality | Risk and Remediation Validation | Ask for remediation steps for a high-risk finding. | The chat provides actionable and relevant remediation guidance. |
| TC_UI_011 | UI Interactions | Copy/Download Functionality | Click the "Copy" or "Download CSV" button in the report section. | The data is copied to clipboard or downloaded as a CSV file. |
| TC_UI_012 | Input Robustness & Error Handling | Clipboard Failure Handling | Attempt to copy report data with clipboard permissions denied. | The UI displays an error or warning about clipboard access. |
| TC_UI_013 | Accessibility & Usability | Usability and UX Feedback | Attempt to use the app on a mobile device or with screen reader. | The UI remains usable and accessible, with no major layout issues. |
| TC_UI_014 | Core Functionality | Explainability and Reasoning | Ask "Why is this issue critical?" for a listed vulnerability. | The chat provides a clear, LLM-generated explanation of the risk. |
| TC_UI_015 | Core Functionality | Prompt Variation - Filter | Enter "/report aws --filter critical" in the chat. | The report only lists critical AWS findings. |
| TC_UI_016 | Input Robustness & Error Handling | Prompt Variation - Vague Prompt | Enter "Show me issues" without specifying a category. | The chat asks for clarification or provides a general summary. |
| TC_UI_017 | Core Functionality | Prompt Variation - Date Range | Enter "/report all --since 2024-01-01". | The report only includes findings since the specified date. |
| TC_UI_018 | Input Robustness & Error Handling | Prompt Robustness - Ambiguous Input | Enter "List stuff" in the chat. | The chat requests clarification or handles the ambiguity gracefully. |
| TC_UI_019 | Input Robustness & Error Handling | Prompt Robustness - Invalid Input | Enter a string of random characters (e.g., "asdf1234!!") in the chat. | The chat displays an error or requests a valid input. |
| TC_UI_020 | Integration & Export | Advanced Prompt - CSV Download | Enter "Download the latest report as CSV" in the chat. | The UI provides a CSV download link or triggers a file download. |
| TC_UI_021 | Core Functionality | Advanced Prompt - Top Risks | Enter "Show me the top 5 risks" in the chat. | The chat lists the top 5 risks based on scan data. |
| TC_UI_022 | Integration & Export | Advanced Prompt - Audit History | Enter "Show audit history for resource X" in the chat. | The chat displays the audit history for the specified resource. |
| TC_UI_023 | Input Robustness & Error Handling | CLI Invalid Command | Use the CLI to run an invalid command (e.g., `make invalid`). | The CLI displays an error message and does not crash. |
| TC_UI_024 | UI Interactions | UI Button Disabled State | Try to click the "Download" button before a scan is complete. | The button is disabled and does not trigger a download. |
| TC_UI_025 | UI Interactions | UI Button Tooltip | Hover over the "Copy" button. | A tooltip appears explaining the button's function. |
| TC_UI_026 | Core Functionality | Summary Section Empty State | View the summary section before any scans are run. | The section displays a message indicating no data is available. |
| TC_UI_027 | UI Interactions | Security Report Pagination | View a report with many findings and navigate using pagination controls. | The UI paginates results and allows navigation between pages. |
| TC_UI_028 | Core Functionality | Risk Remediation Link | Click a remediation link in the chat. | The link opens the relevant documentation or resource. |
| TC_UI_029 | Integration & Export | Download Large Report | Download a report with over 1000 findings. | The download completes successfully and the file is not corrupted. |
| TC_UI_030 | UI Interactions | Clipboard Success Notification | Copy data to clipboard. | The UI displays a success notification. |
| TC_UI_031 | UI Interactions | Clipboard Permission Request | Attempt to copy data when clipboard permissions are not yet granted. | The browser prompts for clipboard access. |
| TC_UI_032 | Accessibility & Usability | Mobile Layout Responsiveness | Open the app on a mobile device and view the layout. | The UI adapts to the screen size without horizontal scrolling. |
| TC_UI_033 | Accessibility & Usability | Keyboard Navigation | Navigate the UI using only the keyboard (Tab, Enter, etc.). | All interactive elements are accessible and usable via keyboard. |
| TC_UI_034 | Accessibility & Usability | Screen Reader Labels | Use a screen reader to navigate the app. | All buttons and fields have appropriate ARIA labels. |
| TC_UI_035 | UI Interactions | Chat Scroll Behavior | Send multiple messages to fill the chat window. | The chat auto-scrolls to the latest message. |
| TC_UI_036 | UI Interactions | Chat Message Timestamp | Check the timestamp on chat messages. | Each message displays a correct timestamp. |
| TC_UI_037 | UI Interactions | Chat Message Order | Send multiple queries in quick succession. | Messages appear in the correct chronological order. |
| TC_UI_038 | UI Interactions | Chat Message Deletion | Delete a message from the chat history. | The message is removed and the UI updates. |
| TC_UI_039 | UI Interactions | Chat Message Edit | Edit a previously sent message. | The message updates and the response is refreshed. |
| TC_UI_040 | Input Robustness & Error Handling | Chat Input Character Limit | Enter a message exceeding the character limit. | The UI prevents further input or displays a warning. |
| TC_UI_041 | UI Interactions | Chat Input Multiline | Enter a multiline message using Shift+Enter. | The input box expands and preserves line breaks. |
| TC_UI_042 | Input Robustness & Error Handling | Chat Input Paste Large Text | Paste a large block of text into the chat input. | The input handles the paste without crashing. |
| TC_UI_043 | UI Interactions | Chat Input Special Characters | Enter special characters (e.g., emojis, symbols) in the chat. | The chat displays them correctly. |
| TC_UI_044 | Input Robustness & Error Handling | Chat Input Language Support | Enter a message in a non-English language. | The chat processes and responds appropriately. |
| TC_UI_045 | UI Interactions | Chat Input Code Block | Enter a code block in the chat input. | The chat displays the code block with formatting. |
| TC_UI_046 | UI Interactions | Chat Input File Attachment | Attach a file if supported. | The file is uploaded and processed or an error is shown if not supported. |
| TC_UI_047 | UI Interactions | Chat Input Drag and Drop | Drag and drop a file into the chat window. | The file is uploaded or an error is shown if not supported. |
| TC_UI_048 | UI Interactions | Chat Input Image Paste | Paste an image into the chat input. | The image is uploaded or an error is shown if not supported. |
| TC_UI_049 | UI Interactions | Chat Input URL Recognition | Enter a URL in the chat input. | The chat recognizes and hyperlinks the URL. |
| TC_UI_050 | UI Interactions | Chat Input Markdown Support | Enter markdown-formatted text. | The chat renders the markdown correctly. |
| TC_UI_051 | UI Interactions | Chat Input Undo/Redo | Use Ctrl+Z and Ctrl+Y in the chat input. | The input supports undo and redo actions. |
| TC_UI_052 | UI Interactions | Chat Input Placeholder Text | View the chat input before typing. | The input displays helpful placeholder text. |
| TC_UI_053 | UI Interactions | Chat Input Focus State | Click into the chat input. | The input highlights to indicate focus. |
| TC_UI_054 | UI Interactions | Chat Input Blur State | Click away from the chat input. | The input loses highlight and saves state. |
| TC_UI_055 | UI Interactions | Chat Input Disabled State | Try to type when the input is disabled (e.g., during loading). | The input is not editable. |
| TC_UI_056 | UI Interactions | Chat Input Loading Indicator | Send a message and observe the input. | A loading spinner or indicator appears until the response is ready. |
| TC_UI_057 | Input Robustness & Error Handling | Chat Input Error State | Trigger an error (e.g., network failure) while sending a message. | The input displays an error and allows retry. |
| TC_UI_058 | Input Robustness & Error Handling | Chat Input Retry | After an error, retry sending the message. | The message is sent successfully if the issue is resolved. |
| TC_UI_059 | UI Interactions | Chat Input Clear Button | Click a clear button in the chat input (if available). | The input is cleared of all text. |
| TC_UI_060 | Parameter & Command Management | Chat Input History Navigation | Use up/down arrows to navigate previous messages. | The input cycles through message history. |
| TC_UI_061 | Parameter & Command Management | Chat Input Autocomplete | Start typing a known command (e.g., /report). | The input suggests autocomplete options. |
| TC_UI_062 | Parameter & Command Management | Chat Input Command List | Type "/" to view available commands. | A dropdown or list of commands appears. |
| TC_UI_063 | Parameter & Command Management | Chat Input Command Help | Hover over a command in the list. | A tooltip or help text appears. |
| TC_UI_064 | Parameter & Command Management | Chat Input Command Execution | Select a command from the list and execute it. | The command runs and the expected result appears. |
| TC_UI_065 | Input Robustness & Error Handling | Chat Input Command Error | Execute a command with missing or invalid arguments. | The chat displays a helpful error message. |
| TC_UI_066 | Parameter & Command Management | Chat Input Command Success | Execute a valid command. | The chat displays a success message or result. |
| TC_UI_067 | Parameter & Command Management | Chat Input Command Chaining | Enter multiple commands in one message (if supported). | Each command is executed in order. |
| TC_UI_068 | Parameter & Command Management | Chat Input Command Scheduling | Schedule a command for later execution (if supported). | The command is scheduled and runs at the specified time. |
| TC_UI_069 | Parameter & Command Management | Chat Input Command Cancellation | Cancel a running command. | The command stops and the UI updates. |
| TC_UI_070 | Parameter & Command Management | Chat Input Command History | View the history of executed commands. | The UI displays a list of past commands. |
| TC_UI_071 | Integration & Export | Chat Input Command Export | Export the command history to a file. | The file downloads successfully. |
| TC_UI_072 | Integration & Export | Chat Input Command Import | Import a list of commands from a file. | The commands are loaded and ready to execute. |
| TC_UI_073 | Input Robustness & Error Handling | Chat Input Command Permissions | Try to execute a restricted command as a non-admin user. | The UI denies access and displays a permission error. |
| TC_UI_074 | Integration & Export | Chat Input Command Logging | Check the logs after executing a command. | The logs record the command and its result. |
| TC_UI_075 | Integration & Export | Chat Input Command Audit Trail | View the audit trail for a command. | The UI displays who ran the command and when. |
| TC_UI_076 | Integration & Export | Chat Input Command Notification | Receive a notification when a scheduled command completes. | The notification appears in the UI. |
| TC_UI_077 | Integration & Export | Chat Input Command Email Alert | Set up an email alert for a command result. | An email is sent when the command finishes. |
| TC_UI_078 | Integration & Export | Chat Input Command Webhook | Set up a webhook for command results. | The webhook is triggered with the result data. |
| TC_UI_079 | Integration & Export | Chat Input Command API Integration | Integrate a command with an external API. | The command sends/receives data from the API. |
| TC_UI_080 | Input Robustness & Error Handling | Chat Input Command Rate Limiting | Exceed the allowed number of commands per minute. | The UI displays a rate limit warning. |
| TC_UI_081 | Input Robustness & Error Handling | Chat Input Command Throttling | Rapidly execute commands in succession. | The UI queues or throttles execution. |
| TC_UI_082 | Input Robustness & Error Handling | Chat Input Command Timeout | Run a long-running command. | The UI displays a timeout error if it takes too long. |
| TC_UI_083 | UI Interactions | Chat Input Command Progress Bar | Execute a command with a progress bar. | The UI shows progress until completion. |
| TC_UI_084 | UI Interactions | Chat Input Command Cancel Button | Click a cancel button during command execution. | The command stops and the UI updates. |
| TC_UI_085 | UI Interactions | Chat Input Command Success Notification | Receive a success notification after a command completes. | The notification appears in the UI. |
| TC_UI_086 | UI Interactions | Chat Input Command Failure Notification | Receive a failure notification after a command fails. | The notification appears in the UI. |
| TC_UI_087 | Parameter & Command Management | Chat Input Command Retry | Retry a failed command. | The command executes again and the result is shown. |
| TC_UI_088 | Parameter & Command Management | Chat Input Command Dependency | Execute a command that depends on another. | The UI enforces dependency order. |
| TC_UI_089 | Input Robustness & Error Handling | Chat Input Command Parameter Validation | Enter invalid parameters for a command. | The UI displays a parameter validation error. |
| TC_UI_090 | Parameter & Command Management | Chat Input Command Parameter Autocomplete | Start typing a parameter for a command. | The UI suggests valid parameters. |
| TC_UI_091 | Parameter & Command Management | Chat Input Command Parameter Help | Hover over a parameter in the command input. | A tooltip or help text appears. |
| TC_UI_092 | Parameter & Command Management | Chat Input Command Parameter Default | Leave a parameter blank. | The command uses the default value. |
| TC_UI_093 | Input Robustness & Error Handling | Chat Input Command Parameter Required | Omit a required parameter. | The UI displays a required field error. |
| TC_UI_094 | Input Robustness & Error Handling | Chat Input Command Parameter Range | Enter a value outside the allowed range. | The UI displays a range validation error. |
| TC_UI_095 | Input Robustness & Error Handling | Chat Input Command Parameter Type | Enter a value of the wrong type. | The UI displays a type validation error. |
| TC_UI_096 | Input Robustness & Error Handling | Chat Input Command Parameter Format | Enter a value in the wrong format. | The UI displays a format validation error. |
| TC_UI_097 | Parameter & Command Management | Chat Input Command Parameter Example | View an example for a parameter. | The UI displays a sample value. |
| TC_UI_098 | Parameter & Command Management | Chat Input Command Parameter Reset | Reset parameters to default values. | The parameters revert to defaults. |
| TC_UI_099 | Parameter & Command Management | Chat Input Command Parameter Save | Save a set of parameters for reuse. | The parameters are saved and can be loaded later. |
| TC_UI_100 | Parameter & Command Management | Chat Input Command Parameter Load | Load a saved set of parameters. | The parameters populate the input fields. | 