# AI Research Assistant

A comprehensive research assistant built with LangChain that can gather information, summarize research, and analyze sources for any research topic.

## 🚀 Features

- **Multi-source Research**: Web search, arXiv, Google Scholar integration
- **Intelligent Memory**: Contextual memory for research history and preferences
- **Document Processing**: Vector storage and semantic search capabilities
- **Interactive Interfaces**: CLI and Streamlit web interface
- **Project Management**: Organize research into projects with reports
- **Data Export**: Export research data in JSON and Excel formats
- **Trend Analysis**: Visualize research trends and patterns

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for real-time data retrieval

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/ai-research-assistant.git
cd ai-research-assistant
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file
```bash
cp .env.example .env
# Edit .env file and add your API key
```

## 📤 GitHub Setup

If you want to create your own repository:

1. **Fix notebook encoding** (prevents empty file issues):
```bash
python fix_notebook.py
```

2. **Upload to GitHub using the automated script**:
```powershell
.\upload_to_github_enhanced.ps1 -GitHubUsername YOUR_USERNAME
```

3. **Manual upload steps** (alternative):
   - See `GITHUB_UPLOAD_GUIDE.md` for detailed instructions

## 🚀 Usage

### Option 1: Jupyter Notebook (Recommended)
Open and run `custom_research_assistant.ipynb` in Jupyter Notebook or VS Code.

### Option 2: Streamlit Web Interface
```bash
streamlit run research_app.py
```

### Option 3: Command Line Interface
```python
from research_assistant import ResearchAssistant, ResearchInterface

# Initialize the assistant
assistant = ResearchAssistant(os.getenv("OPENAI_API_KEY"))

# Start interactive session
interface = ResearchInterface(assistant)
interface.interactive_session()
```

## 📊 Key Capabilities

1. **Smart Research**: Breaks down complex queries into smaller searches
2. **Memory System**: Remembers preferences and research history
3. **Source Integration**: Academic papers, web sources, news articles
4. **Document Analysis**: Process and query your own documents
5. **Project Organization**: Manage multiple research projects
6. **Report Generation**: Automated research reports with proper structure
7. **Data Export**: Multiple formats for further analysis
8. **Cost Management**: Track API usage and costs

## 🔧 Configuration

The assistant can be configured through environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `LANGCHAIN_TRACING_V2`: Enable LangSmith tracing (optional)
- `LANGCHAIN_API_KEY`: LangSmith API key (optional)
- `LANGCHAIN_PROJECT`: LangSmith project name (optional)

## 📁 Project Structure

```
ai-research-assistant/
├── custom_research_assistant.ipynb  # Main notebook
├── research_app.py                  # Streamlit web interface
├── requirements.txt                 # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore file
└── README.md                       # This file
```

## 🔒 Security

- Never commit your `.env` file or API keys to the repository
- The `.gitignore` file is configured to exclude sensitive files
- Use environment variables for all API keys and secrets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Cost Management

This application uses the OpenAI API which charges per token. Monitor your usage:
- The assistant tracks costs for each query
- Set usage limits in your OpenAI account
- Review the cost before running large research projects

## 🔧 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your OpenAI API key is correctly set in the `.env` file
2. **Module Not Found**: Run `pip install -r requirements.txt` to install all dependencies
3. **Rate Limiting**: The application handles rate limits automatically, but you may need to wait
4. **Memory Issues**: Large documents may require more system memory

### Getting Help

- Check the notebook for detailed examples
- Review the error messages for specific issues
- Ensure all dependencies are properly installed

## 🎯 Example Use Cases

- **Academic Research**: Literature reviews, citation analysis
- **Business Intelligence**: Market research, competitive analysis
- **Content Creation**: Background research for articles or reports
- **Learning**: Exploring new topics with guided research
- **Professional Development**: Staying updated with industry trends
