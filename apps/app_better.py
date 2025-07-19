#!/usr/bin/env python3
"""
Health RAG Chatbot - Better Web Application
Using Streamlit native components for better compatibility
"""

import streamlit as st
import sys
import os
import warnings

# Suppress warnings
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

# Custom CSS for styling
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
    
    /* Sidebar styling */
    .sidebar-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .feature-card:nth-child(2) {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
    }
    
    .feature-card:nth-child(3) {
        background: linear-gradient(135deg, #45b7d1 0%, #96c93d 100%);
    }
    
    .metric-container {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
        padding: 0.5rem;
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
    }
    
    .metric-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
    }
    
    .metric-content {
        flex: 1;
    }
    
    .metric-value {
        font-size: 1.2rem;
        font-weight: bold;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.8;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_rag_system():
    """Load the RAG system"""
    try:
        from rag_system import HealthRAGSystem
        return HealthRAGSystem()
    except Exception as e:
        st.error(f"Error loading RAG system: {e}")
        return None

def create_stats_section():
    """Create stats section using Streamlit components"""
    st.markdown("### 📊 Database Statistics")
    
    # Create a styled container
    with st.container():
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        
        # Metric 1: Diseases
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("🏥")
        with col2:
            st.markdown("**2,235+**")
            st.markdown("*Diseases & Conditions*")
        
        # Metric 2: Document Chunks
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("📄")
        with col2:
            st.markdown("**31,121**")
            st.markdown("*Document Chunks*")
        
        # Metric 3: Database Size
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("💾")
        with col2:
            st.markdown("**73MB**")
            st.markdown("*Vector Database*")
        
        # Progress bar
        st.markdown("**Database Coverage**")
        st.progress(0.95)
        st.markdown("*95% Complete*")
        
        st.markdown('</div>', unsafe_allow_html=True)

def create_features_section():
    """Create features section using Streamlit components"""
    st.markdown("### ✨ Key Features")
    
    # Feature 1: Mayo Clinic Data
    with st.container():
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("🏥")
        with col2:
            st.markdown("**Mayo Clinic Data**")
            st.markdown("Trusted medical information from one of the world's leading healthcare institutions")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature 2: Fast Responses
    with st.container():
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("⚡")
        with col2:
            st.markdown("**Fast Responses**")
            st.markdown("Instant AI-powered answers with intelligent context retrieval")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature 3: Accurate Results
    with st.container():
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("🎯")
        with col2:
            st.markdown("**Accurate Results**")
            st.markdown("RAG-powered responses with source attribution")
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🏥 Health RAG Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Get accurate health information from Mayo Clinic\'s trusted medical database</p>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    if 'system_loaded' not in st.session_state:
        st.session_state.system_loaded = False
    
    # Sidebar
    with st.sidebar:
        st.markdown('<h2 class="sidebar-header">📊 System Dashboard</h2>', unsafe_allow_html=True)
        
        # System Status
        if not st.session_state.system_loaded:
            with st.spinner("Loading AI system..."):
                st.session_state.rag_system = load_rag_system()
                if st.session_state.rag_system:
                    st.session_state.system_loaded = True
                    st.success("✅ System Online")
                    st.info("AI system loaded successfully!")
                else:
                    st.error("❌ Failed to load system")
                    return
        else:
            st.success("✅ System Online")
            st.info("Ready to answer your questions!")
        
        # Stats Section
        create_stats_section()
        
        # Features Section
        create_features_section()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat area
    st.header("💬 Chat")
    
    # Display messages
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
    
    # Question input
    question = st.text_area(
        "Ask a health question:",
        placeholder="e.g., What are the symptoms of diabetes? How to treat high blood pressure?",
        height=100
    )
    
    # Send button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        send_button = st.button("🚀 Send Question", type="primary", use_container_width=True)
    
    # Process question
    if send_button and question.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": question.strip()})
        
        # Get response
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
                
                # Rerun to show new messages
                st.rerun()
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
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