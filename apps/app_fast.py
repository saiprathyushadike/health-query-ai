#!/usr/bin/env python3
"""
Health Query AI - Fast Version
Optimized for quick responses and screen recording
"""

import streamlit as st
import sys
import os
import warnings
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import time

# Suppress warnings
warnings.filterwarnings("ignore")

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Page configuration
st.set_page_config(
    page_title="🏥 Health Query AI - Fast",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean, minimal CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.3rem 0;
        border-left: 3px solid;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    .fast-badge {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-left: 1rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_fast_rag_system():
    """Load the fast RAG system"""
    try:
        from rag_system_fast import FastHealthRAGSystem
        return FastHealthRAGSystem()
    except Exception as e:
        st.error(f"Error loading fast RAG system: {e}")
        return None

def get_health_facts():
    """Get list of health facts"""
    return [
        "The human body contains enough iron to make a 3-inch nail.",
        "Your heart beats about 100,000 times every day.",
        "Your brain uses 20% of your body's total energy.",
        "The human body sheds about 600,000 particles of skin every hour.",
        "Your stomach acid is strong enough to dissolve razor blades.",
        "Your body has enough blood vessels to circle the Earth 2.5 times.",
        "Your eyes can distinguish about 10 million different colors.",
        "The human body produces enough heat in 30 minutes to boil a gallon of water."
    ]

def create_interactive_stats():
    """Create interactive health statistics"""
    # Sample health data
    data = {
        'Condition': ['Diabetes', 'Hypertension', 'Heart Disease', 'Obesity', 'Asthma'],
        'Prevalence (%)': [9.4, 32.0, 6.7, 42.4, 7.7],
        'Risk Level': ['High', 'High', 'High', 'Medium', 'Medium']
    }
    df = pd.DataFrame(data)
    
    fig = px.bar(df, x='Condition', y='Prevalence (%)', 
                 color='Risk Level',
                 title='Common Health Conditions Prevalence',
                 color_discrete_map={'High': '#ff6b6b', 'Medium': '#4ecdc4'})
    
    fig.update_layout(
        xaxis_title="Health Condition",
        yaxis_title="Prevalence (%)",
        showlegend=True
    )
    
    return fig

def create_did_you_know():
    """Create rotating health facts"""
    facts = get_health_facts()
    
    # Use session state to rotate facts
    if 'fact_index' not in st.session_state:
        st.session_state.fact_index = 0
    
    # Auto-rotate every 3 seconds
    if 'last_rotation' not in st.session_state:
        st.session_state.last_rotation = time.time()
    
    current_time = time.time()
    if current_time - st.session_state.last_rotation > 3:
        st.session_state.fact_index = (st.session_state.fact_index + 1) % len(facts)
        st.session_state.last_rotation = current_time
    
    current_fact = facts[st.session_state.fact_index]
    
    st.markdown(f"""
    <div class="did-you-know">
        <h3>💡 Did You Know?</h3>
        <p>{current_fact}</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = load_fast_rag_system()
    
    # Main header
    st.markdown("""
    <div class="main-header">
        🏥 Health Query AI <span class="fast-badge">FAST MODE</span>
    </div>
    <div class="sub-header">
        AI-powered health information with optimized responses | Powered by Local LLM
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📊 Stats", "💡 Did You Know", "🚀 Fast Mode"])
    
    with tab1:
        st.markdown("### Ask Health Questions")
        st.markdown("Get instant, accurate health information powered by AI.")
        
        # Chat interface
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a health question..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("🤖 Thinking..."):
                    if st.session_state.rag_system:
                        response = st.session_state.rag_system.answer_question(prompt)
                        answer = response.get('answer', 'Sorry, I could not process your question.')
                        
                        # Display answer
                        st.markdown(answer)
                        
                        # Show sources if available
                        sources = response.get('sources', [])
                        if sources:
                            with st.expander("📚 Sources"):
                                for i, source in enumerate(sources, 1):
                                    st.markdown(f"**Source {i}:** {source.get('metadata', {}).get('title', 'Unknown')}")
                                    st.markdown(f"*{source.get('content', '')}*")
                    else:
                        st.error("RAG system not loaded. Please check the setup.")
            
            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": answer})
    
    with tab2:
        st.markdown("### Health Statistics")
        st.markdown("Interactive health data and insights.")
        
        # Health statistics
        fig = create_interactive_stats()
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Response Time", "2-5 seconds", "⚡ Fast")
        with col2:
            st.metric("Knowledge Base", "3+ Diseases", "🏥 Medical")
        with col3:
            st.metric("AI Model", "Llama2", "🤖 Local")
    
    with tab3:
        st.markdown("### Health Facts")
        st.markdown("Interesting health facts that rotate automatically.")
        
        create_did_you_know()
        
        st.markdown("---")
        st.markdown("""
        ### Quick Health Tips
        - **Stay Hydrated**: Drink 8 glasses of water daily
        - **Exercise**: 30 minutes of moderate activity most days
        - **Sleep**: Aim for 7-9 hours of quality sleep
        - **Nutrition**: Eat a balanced diet with plenty of fruits and vegetables
        """)
    
    with tab4:
        st.markdown("### 🚀 Fast Mode Features")
        st.markdown("This version is optimized for quick responses and screen recording.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### ⚡ Speed Optimizations
            - **Reduced Context**: Smaller context window (2048 tokens)
            - **Single Document**: Retrieve only 1 most relevant document
            - **Focused Prompts**: Shorter, more direct prompts
            - **Limited Response**: Max 256 tokens per response
            - **Optimized Settings**: Lower temperature and focused parameters
            """)
        
        with col2:
            st.markdown("""
            #### 🎯 Perfect for Demos
            - **2-5 second responses** (vs 20-40 seconds)
            - **Concise answers** for quick understanding
            - **Fast loading** for screen recordings
            - **Reliable performance** for live demos
            - **Local processing** for privacy
            """)
        
        st.markdown("---")
        st.markdown("""
        #### 🎬 Demo Questions to Try
        - "What are the symptoms of diabetes?"
        - "How to manage high blood pressure?"
        - "What causes heart disease?"
        - "Treatment for dark circles"
        """)
        
        # System status
        if st.session_state.rag_system:
            info = st.session_state.rag_system.get_database_info()
            st.success(f"✅ System Status: Ready (Fast Mode)")
            st.info(f"📊 Database: {info.get('total_documents', 0)} documents loaded")
        else:
            st.error("❌ System Status: Not Ready")

if __name__ == "__main__":
    main() 