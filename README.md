# AI Web Test Automation Platform

> **Transform natural language instructions into executable Playwright tests using AI**

An intelligent test automation system that converts plain English instructions into executable browser tests using LangGraph workflows and LLM-powered code generation.

---

## ✨ Features

### Core Capabilities
- 🗣️ **Natural Language Processing** - Write tests in plain English
- 🤖 **AI-Powered Code Generation** - Automatic Playwright Python code creation
- 🔄 **LangGraph Workflow Engine** - Stateful test execution pipeline
- 🎯 **Adaptive DOM Mapping** - Multiple fallback selectors for robustness
- 🔁 **Error Handling & Retry Logic** - Automatic recovery mechanisms
- 📊 **Excel/CSV Data Storage** - Complete test history tracking
- 📈 **Real-time Analytics Dashboard** - Performance metrics and insights
- 👁️ **Visible Browser Mode** - Watch tests execute in real-time

### Advanced Features
- Multi-site search support (Google, YouTube, Amazon)
- Cookie consent handling
- Login status detection
- Automatic screenshot capture on errors
- Slow-motion execution for demos
- JSON audit logs
- Exportable reports

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Input (Natural Language)            │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              LangGraph Workflow Engine                       │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Parser  │→ │  State   │→ │   Code   │→ │  Execute │    │
│  │(3 retry)│  │ Tracker  │  │Generator │  │ (2 retry)│    │
│  └─────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Playwright Test Execution                       │
│         (Visible Browser + Slow Motion)                      │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Data Storage & Analytics                        │
│    Excel Files + JSON Logs + Screenshots                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Groq API key (for LLM)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ai-web-test-agent.git
cd ai-web-test-agent

# 2. Create virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install chromium

# 5. Configure API key
echo GROQ_API_KEY=your_groq_api_key_here > .env

# 6. Run the application
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

---

## 📝 Usage Examples

### Example 1: Simple Google Search

```
Instruction: open browser search for python playwright tutorial
```

**What happens:**
1. Browser opens (visible mode)
2. Navigates to Google
3. Accepts cookie consent
4. Searches for "python playwright tutorial"
5. Displays results for 20 seconds

### Example 2: YouTube Video Search

```
Instruction: open browser go to youtube.com
             search automation testing
             wait 3 seconds
             click first video
```

### Example 3: Amazon Product Search

```
Instruction: open browser go to amazon.in
             search wireless mouse
```

### Example 4:  Login Test

```
Instruction: open browser go to https://login-admin-testing.vercel.app/
             type admin into #username
             type admin123 into #password
             click #loginBtn
```

---

## 🛠️ Technology Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3.10+ | Core application |
| **UI Framework** | Streamlit 1.32.0 | Web interface |
| **Workflow Engine** | LangGraph 0.0.20 | State management |
| **Browser Automation** | Playwright 1.48.0 | Test execution |
| **LLM Provider** | Groq API | Code generation |
| **LLM Model** | llama-3.3-70b-versatile | Primary model |
| **Data Processing** | Pandas 2.2.0 | Data manipulation |
| **Visualization** | Plotly 5.18.0 | Charts & graphs |
| **Data Storage** | Excel/CSV + JSON | Test history |

---

## 📁 Project Structure

```
ai-web-test-agent/
│
├── streamlit_app.py              # Main Streamlit application
├── requirements.txt              # Python dependencies
├── .env                          # API keys (create this)
├── README.md                     # This file
│
├── app/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── test_agent_enhanced.py    # LangGraph workflow
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── llm.py                    # Groq API configuration
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   └── excel_data_manager.py     # Data storage manager
│   │
│   ├── executor/
│   │   ├── __init__.py
│   │   └── python_executor.py        # Playwright code generator
│   │
│   └── generated_tests/              # Auto-generated test files
│
├── test_logs/                        # JSON execution logs
├── screenshots/                      # Error screenshots
├── test_history.xlsx                 # Main data file
└── venv/                             # Virtual environment
```

---

## 🔄 LangGraph Workflow

### State Management

```python
TestState = {
    "user_instruction": str,      # User's natural language input
    "parsed_steps": list,          # Parsed test steps
    "parsing_status": str,         # success/failed
    "browser_open": bool,          # Browser state
    "current_url": str,            # Active URL
    "logged_in": bool,             # Authentication status
    "generated_code": str,         # Python test code
    "code_file_path": str,         # Saved file location
    "execution_status": str,       # Test result
    "execution_output": str,       # Console output
    "execution_errors": str,       # Error messages
    "retry_count": int,            # Retry attempts
    "test_passed": bool            # Final result
}
```

### Workflow Steps

1. **Parse** (Node 1)
   - Converts natural language to JSON steps
   - 3 retry attempts with error handling
   - JSON validation and cleanup

2. **Track State** (Node 2)
   - Monitors browser state
   - Tracks URL changes
   - Detects login status

3. **Generate Code** (Node 3)
   - Creates Python Playwright code
   - Adds error handling
   - Includes adaptive selectors

4. **Save Code** (Node 4)
   - Saves to `app/generated_tests/`
   - Timestamps filename
   - UTF-8 encoding

5. **Execute** (Node 5)
   - Runs test in visible browser
   - 2 retry attempts on failure
   - Captures screenshots on errors

---

## 📊 Data Storage

### Excel File Structure (`test_history.xlsx`)

| Column | Type | Description |
|--------|------|-------------|
| test_id | string | Unique identifier (timestamp) |
| timestamp | datetime | Execution time |
| instruction | string | User's input |
| status | string | passed/failed/timeout |
| passed | boolean | Test result |
| duration_seconds | float | Execution time |
| steps_count | int | Number of steps |
| browser_opened | boolean | Browser state |
| url_visited | string | Target URL |
| login_checked | boolean | Login check performed |
| login_status | string | Authentication state |
| screenshots_taken | int | Screenshot count |
| errors | string | Error messages |
| code_file_path | string | Generated test path |
| log_file_path | string | JSON log path |

### JSON Logs (`test_logs/`)

Detailed execution logs with:
- Complete state information
- Full console output
- Generated code
- Browser state tracking
- Metadata and timestamps

---

## 🎯 Supported Actions

| Action | Description | Example |
|--------|-------------|---------|
| `OPEN_BROWSER` | Navigate to URL | `open browser go to example.com` |
| `SEARCH` | Search on current page | `search for keyword` |
| `CLICK` | Click element | `click the submit button` |
| `TYPE` | Type into input field | `type text into field` |
| `CHECK_LOGIN` | Verify auth status | `check if logged in` |
| `WAIT` | Pause execution | `wait 3 seconds` |
| `SCREENSHOT` | Capture screenshot | `take screenshot name.png` |
| `ASSERT_TEXT` | Verify text presence | `verify page contains text` |

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
```

### LLM Configuration (`app/config/llm.py`)

The system uses Groq API with fallback logic:

1. **Primary:** llama-3.3-70b-versatile (fast, powerful)
2. **Fallback:** gemma2-9b-it (smaller, reliable)
3. **Local Fallback:** Ollama gemma:2b (optional)

---

## 📈 Analytics Dashboard

The built-in dashboard provides:

- **Total Executions:** Count of all tests
- **Success Rate:** Percentage of passed tests
- **Average Duration:** Mean execution time
- **Total Steps:** Cumulative step count
- **Pass/Fail Distribution:** Pie chart
- **Timeline Chart:** Duration trends over time
- **Activity Metrics:** Login checks, screenshots

---
---

## 🧪 Testing

### Run a Test via UI

1. Open `http://localhost:8501`
2. Navigate to "Execute Tests"
3. Enter instruction or click quick action
4. Click "Execute Test"
5. View results in real-time

### Test via Python

```python
from app.agents.test_agent_enhanced import agent

result = agent.invoke({
    "user_instruction": "open browser search for AI",
    "parsed_steps": [],
    "parsing_status": "",
    # ... other state fields
})

print(f"Test passed: {result['test_passed']}")
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** `No module named 'streamlit'`
```bash
pip install streamlit
```

**Issue:** `Groq API error`
- Check your API key in `.env`
- Verify internet connection
- Try fallback model

**Issue:** `Browser not found`
```bash
playwright install chromium
```

**Issue:** `Import errors`
- Ensure you're in project root
- Check all `__init__.py` files exist

### Debug Mode

Enable verbose logging:

```python
# In streamlit_app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🔐 Security Notes

- Never commit `.env` file to Git
- Keep API keys secure
- Review generated code before execution
- Use sandboxed environments for untrusted tests

---

## 🚧 Roadmap

### Planned Features

- [ ] Multi-browser support (Firefox, Safari)
- [ ] Parallel test execution
- [ ] CI/CD integration (GitHub Actions)
- [ ] Custom selector training
- [ ] Video recording
- [ ] Mobile testing
- [ ] API testing support
- [ ] Database integration (PostgreSQL)
- [ ] Team collaboration features
- [ ] Schedule recurring tests

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black app/
```


## 👥 Authors

- **Abhinav Padige** 

---

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) - Browser automation
- [LangGraph](https://github.com/langchain-ai/langgraph) - Workflow engine
- [Groq](https://groq.com/) - LLM API
- [Streamlit](https://streamlit.io/) - Web framework
- Anthropic Claude - Development assistance

---

## 📞 Support
- **Email:** abhinavpadige06@gmail.com

---

## 📊 Project Status

**Current Version:** 1.0.0  
**Status:** Active Development  
**Last Updated:** February 2026

---

## 🌟 Star History

If you find this project helpful, please consider giving it a ⭐ on GitHub!

---

<div align="center">

</div>
