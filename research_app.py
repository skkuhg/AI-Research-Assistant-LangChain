import os
import sys
from pathlib import Path

# Add the current directory to the path to import from the notebook
sys.path.append(str(Path(__file__).parent))

# Import necessary modules
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

# Import from the notebook (this would typically be in a separate module)
# For now, we'll recreate the necessary classes here
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import requests
from bs4 import BeautifulSoup
import arxiv
import tiktoken
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

# Load environment variables
load_dotenv()

# Note: Import ResearchAssistant from the notebook or create a separate module
# For this example, we'll assume it's imported from a separate module
try:
    from custom_research_assistant import ResearchAssistant
except ImportError:
    # If the import fails, we'll create a simplified version
    class ResearchAssistant:
        def __init__(self, api_key):
            self.api_key = api_key
            # Simplified implementation
        
        def research(self, query, include_analysis=True):
            return {
                'query': query,
                'findings': 'Research functionality not available - please run the notebook first',
                'sources': [],
                'cost': 0.0,
                'tokens_used': 0
            }

def create_streamlit_app():
    st.set_page_config(
        page_title="AI Research Assistant", 
        page_icon="🔬", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'assistant' not in st.session_state:
        try:
            st.session_state.assistant = ResearchAssistant(os.environ["OPENAI_API_KEY"])
        except Exception as e:
            st.error(f"Failed to initialize assistant: {e}")
            return
            
    if 'research_history' not in st.session_state:
        st.session_state.research_history = []
    
    # Header
    st.markdown('<h1 class="main-header">🔬 AI Research Assistant</h1>', unsafe_allow_html=True)
    st.markdown("Your intelligent companion for academic research and knowledge discovery")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Research mode
        research_mode = st.selectbox(
            "Research Mode",
            ["Comprehensive", "Quick Overview", "Academic Focus", "Technical Deep Dive"]
        )
        
        # Update preferences
        if st.button("Update Preferences"):
            st.session_state.assistant.memory.update_preferences('summary_style', research_mode.lower())
            st.success("Preferences updated!")
        
        st.header("📊 Session Stats")
        stats = st.session_state.assistant.memory.session_stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Queries", stats['queries_conducted'])
        with col2:
            st.metric("Cost", f"${stats['total_cost']:.4f}")
        
        st.header("📚 Research History")
        if st.session_state.research_history:
            for i, entry in enumerate(st.session_state.research_history[-5:]):
                with st.expander(f"Query {i+1}"):
                    st.text(entry['topic'][:50] + "...")
                    st.caption(f"Time: {entry['timestamp']}")
                    st.caption(f"Cost: ${entry.get('cost', 0):.4f}")
        else:
            st.info("No research history yet")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Research", 
        "📝 Summarize", 
        "📚 Recommendations", 
        "📈 Trends",
        "📄 Documents"
    ])
    
    with tab1:
        st.header("Research Query")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            query = st.text_area(
                "Enter your research question:", 
                height=100,
                placeholder="e.g., What are the latest developments in quantum computing?"
            )
        with col2:
            include_analysis = st.checkbox("Include Analysis", value=True)
            max_results = st.slider("Max Results", 1, 10, 5)
        
        if st.button("🔍 Start Research", type="primary"):
            if query:
                with st.spinner("🔍 Researching... This may take a moment."):
                    result = st.session_state.assistant.research(query, include_analysis)
                    
                    # Add to history
                    st.session_state.research_history.append({
                        'topic': query,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                        'result': result,
                        'cost': result.get('cost', 0)
                    })
                    
                    # Display results
                    if not result.get('error'):
                        st.success("✅ Research completed!")
                        
                        # Main findings
                        with st.expander("📊 Research Findings", expanded=True):
                            st.write(result['findings'])
                        
                        # Sources and metadata
                        col1, col2 = st.columns(2)
                        with col1:
                            with st.expander("📚 Sources"):
                                for source in result['sources']:
                                    st.write(f"• {source}")
                        
                        with col2:
                            with st.expander("📈 Metadata"):
                                st.write(f"**Tokens used:** {result['tokens_used']}")
                                st.write(f"**Cost:** ${result['cost']:.4f}")
                                st.write(f"**Timestamp:** {result['timestamp']}")
                        
                        # Analysis if available
                        if include_analysis and 'analysis' in result:
                            with st.expander("🧠 Analysis"):
                                analysis = result['analysis']
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Word Count", analysis['word_count'])
                                with col2:
                                    st.metric("Has Citations", analysis['has_citations'])
                                with col3:
                                    st.metric("Confidence Indicators", len(analysis['confidence_indicators']))
                    else:
                        st.error(f"❌ Research failed: {result['findings']}")
            else:
                st.warning("Please enter a research query.")
    
    with tab2:
        st.header("Topic Summarization")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            topic = st.text_input("Topic to summarize:", placeholder="e.g., Machine Learning in Healthcare")
        with col2:
            style = st.select_slider(
                "Summary style:",
                options=["Brief", "Comprehensive", "Technical"],
                value="Comprehensive"
            )
        
        if st.button("📝 Generate Summary"):
            if topic:
                with st.spinner("📝 Generating summary..."):
                    summary_query = f"Create a {style.lower()} summary on the topic: {topic}"
                    result = st.session_state.assistant.research(summary_query)
                    
                    st.markdown("### Summary")
                    st.write(result['findings'])
                    
                    st.info(f"Cost: ${result['cost']:.4f} | Tokens: {result['tokens_used']}")
    
    with tab3:
        st.header("Source Recommendations")
        
        rec_topic = st.text_input("Topic for recommendations:", placeholder="e.g., Natural Language Processing")
        
        if st.button("📖 Get Recommendations"):
            if rec_topic:
                with st.spinner("📖 Finding sources..."):
                    rec_query = f"Recommend high-quality academic sources, books, and resources for: {rec_topic}"
                    result = st.session_state.assistant.research(rec_query)
                    
                    st.markdown("### Recommended Sources")
                    st.write(result['findings'])
                    
                    st.info(f"Cost: ${result['cost']:.4f}")
    
    with tab4:
        st.header("Research Trend Analysis")
        
        trend_topic = st.text_input("Topic for trend analysis:", placeholder="e.g., Artificial Intelligence Ethics")
        
        if st.button("📈 Analyze Trends"):
            if trend_topic:
                with st.spinner("📈 Analyzing trends..."):
                    trend_query = f"Analyze current research trends, recent developments, and future directions in: {trend_topic}"
                    result = st.session_state.assistant.research(trend_query)
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("### Trend Analysis")
                        st.write(result['findings'])
                    
                    with col2:
                        st.markdown("### Publication Trend (Sample)")
                        # Sample data for visualization
                        years = list(range(2019, 2025))
                        publications = [45, 52, 68, 85, 92, 105]
                        
                        fig = px.line(
                            x=years, 
                            y=publications,
                            title=f"Research Publications: {trend_topic}",
                            labels={'x': 'Year', 'y': 'Publications'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.header("Document Management")
        
        # Document upload
        st.subheader("Add Documents")
        
        # URL input
        url = st.text_input("Add document from URL:")
        if st.button("Add from URL"):
            if url:
                with st.spinner("Adding document..."):
                    result = st.session_state.assistant.doc_processor.add_document_from_url(url)
                    if "Successfully" in result:
                        st.success(result)
                    else:
                        st.error(result)
        
        # File upload
        uploaded_file = st.file_uploader("Upload document", type=['txt', 'pdf', 'docx'])
        if uploaded_file and st.button("Process Uploaded File"):
            # Simple text extraction (you'd want more robust handling for PDF/DOCX)
            if uploaded_file.type == "text/plain":
                content = str(uploaded_file.read(), "utf-8")
                metadata = [{"source": uploaded_file.name, "type": "uploaded_file"}]
                st.session_state.assistant.doc_processor.process_documents([content], metadata)
                st.success(f"Processed {uploaded_file.name}")
        
        # Document query
        st.subheader("Query Documents")
        doc_query = st.text_input("Query your documents:")
        if st.button("Search Documents"):
            if doc_query:
                result = st.session_state.assistant.doc_processor.query_documents(doc_query)
                st.write(result)
        
        # Document stats
        st.subheader("Document Statistics")
        stats = st.session_state.assistant.doc_processor.get_document_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Documents", stats.get('total_documents', 0))
        with col2:
            st.metric("Total Chunks", stats.get('total_chunks', 0))

# Run the Streamlit app
if __name__ == "__main__":
    create_streamlit_app()
