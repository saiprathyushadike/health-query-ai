#!/usr/bin/env python3
"""
Health RAG Chatbot - Web Application
Beautiful web interface for the Mayo Clinic RAG chatbot
"""

import streamlit as st
import sys
import os
import time
import warnings
from datetime import datetime

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Page configuration
st.set_page_config(
    page_title="🏥 Health RAG Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    
    /* Enhanced Sidebar Styling */
    .sidebar-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1.5rem;
        text-align: center;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .stat-item {
        display: flex;
        align-items: center;
        margin: 0.8rem 0;
        padding: 0.5rem;
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stat-item:hover {
        background: rgba(255,255,255,0.2);
        transform: translateX(5px);
    }
    
    .stat-icon {
        font-size: 1.5rem;
        margin-right: 0.8rem;
        min-width: 30px;
    }
    
    .stat-content {
        flex: 1;
    }
    
    .stat-value {
        font-size: 1.2rem;
        font-weight: bold;
        color: white;
        margin: 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
        margin: 0;
    }
    
    .features-container {
        margin: 1.5rem 0;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .feature-card:nth-child(2) {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
    }
    
    .feature-card:nth-child(3) {
        background: linear-gradient(135deg, #45b7d1 0%, #96c93d 100%);
    }
    
    .feature-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .feature-icon {
        font-size: 1.8rem;
        margin-right: 0.8rem;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: bold;
        margin: 0;
    }
    
    .feature-description {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0;
        line-height: 1.4;
    }
    
    .system-status {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #4CAF50;
        margin-right: 0.5rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .clear-chat-btn {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }
    
    .clear-chat-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Progress bar styling */
    .progress-container {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        height: 6px;
        background: rgba(255,255,255,0.3);
        border-radius: 3px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        border-radius: 3px;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_rag_system():
    """Load the RAG system (cached for performance)"""
    try:
        from rag_system import HealthRAGSystem
        return HealthRAGSystem()
    except Exception as e:
        st.error(f"Error loading RAG system: {e}")
        return None

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    if 'system_loaded' not in st.session_state:
        st.session_state.system_loaded = False
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0

def create_interactive_stats():
    """Create interactive stats display using Streamlit components"""
    # Create a container for stats
    with st.container():
        st.markdown("""
        <div class="stats-container">
            <h3 style="color: white; text-align: center; margin-bottom: 1rem;">📊 Database Statistics</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Use columns for better layout
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("🏥")
        with col2:
            st.markdown("**2,235+**")
            st.markdown("*Diseases & Conditions*")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("📄")
        with col2:
            st.markdown("**31,121**")
            st.markdown("*Document Chunks*")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("💾")
        with col2:
            st.markdown("**73MB**")
            st.markdown("*Vector Database*")
        
        # Progress bar
        st.markdown("**Database Coverage**")
        st.progress(0.95)
        st.markdown("*95% Complete*")

def create_interactive_features():
    """Create interactive features display using Streamlit components"""
    st.markdown("**✨ Key Features**")
    
    # Feature 1
    with st.container():
        st.markdown("""
        <div class="feature-card">
            <div class="feature-header">
                <div class="feature-icon">🏥</div>
                <div class="feature-title">Mayo Clinic Data</div>
            </div>
            <div class="feature-description">Trusted medical information from one of the world's leading healthcare institutions</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature 2
    with st.container():
        st.markdown("""
        <div class="feature-card">
            <div class="feature-header">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Fast Responses</div>
            </div>
            <div class="feature-description">Instant AI-powered answers with intelligent context retrieval</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature 3
    with st.container():
        st.markdown("""
        <div class="feature-card">
            <div class="feature-header">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Accurate Results</div>
            </div>
            <div class="feature-description">RAG-powered responses with source attribution</div>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🏥 Health RAG Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Get accurate health information from Mayo Clinic\'s trusted medical database</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<h2 class="sidebar-header">📊 System Dashboard</h2>', unsafe_allow_html=True)
        
        # System Status
        if not st.session_state.system_loaded:
            with st.spinner("Loading AI system..."):
                st.session_state.rag_system = load_rag_system()
                if st.session_state.rag_system:
                    st.session_state.system_loaded = True
                    st.success("✅ System Online - AI system loaded successfully!")
                else:
                    st.error("❌ Failed to load system")
                    return
        else:
            st.success("✅ System Online - Ready to answer your questions!")
        
        # Interactive Stats
        create_interactive_stats()
        
        # Interactive Features
        create_interactive_features()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.input_key += 1
            st.rerun()
    
    # Main chat interface
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            # Display chat messages
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f'''
                    <div class="chat-message user-message">
                        <strong>You:</strong> {message["content"]}
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div class="chat-message bot-message">
                        <strong>🏥 Health Bot:</strong> {message["content"]}
                    </div>
                    ''', unsafe_allow_html=True)
        
        # Input area
        st.markdown("---")
        
        # Question input with dynamic key
        question = st.text_area(
            "Ask a health question:",
            placeholder="e.g., What are the symptoms of diabetes? How to treat high blood pressure?",
            height=100,
            key=f"question_input_{st.session_state.input_key}"
        )
        
        # Send button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            send_button = st.button("🚀 Send Question", type="primary", use_container_width=True)
        
        # Process question
        if send_button and question.strip():
            # Add user message
            st.session_state.messages.append({"role": "user", "content": question.strip()})
            
            # Get bot response
            with st.spinner("🤔 Thinking..."):
                try:
                    result = st.session_state.rag_system.answer_question(question.strip())
                    
                    # Extract answer
                    if isinstance(result, dict) and 'answer' in result:
                        answer = result['answer']
                    else:
                        answer = str(result)
                    
                    # Add bot message
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    # Increment input key to clear the input
                    st.session_state.input_key += 1
                    
                    # Rerun to show new messages
                    st.rerun()
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.session_state.input_key += 1
                    st.rerun()
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
            <p>🏥 Powered by Mayo Clinic Data | 🤖 RAG + Ollama | ⚡ Fast & Accurate</p>
            <p>Built with ❤️ using Streamlit, LangChain, and FAISS</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 