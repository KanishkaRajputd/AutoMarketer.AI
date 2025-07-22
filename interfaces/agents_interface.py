import streamlit as st
from interfaces.chat_interface import show_chat_interface

def show_agents_interface():
    """Display the agents interface with sidebar navigation"""
    
    # Custom CSS for the agents interface
    st.markdown("""
    <style>
        .agent-main-content {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 2rem;
            border-radius: 10px;
            min-height: 500px;
        }
        
        .agent-header {
            color: #667eea;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        .agent-description {
            color: #4a5568;
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .input-container {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        
        .generate-button {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
            padding: 0.75rem 2rem;
            border: none;
            border-radius: 25px;
            font-weight: 600;
            cursor: pointer;
            font-size: 1rem;
            width: 100%;
            margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar with agents display
    with st.sidebar:
        st.markdown("### 🎯 **Available Agents**")
        
        # Back button in sidebar
        if st.button("← Back to Home", key="back_button", use_container_width=True):
            st.session_state.show_agents = False
            st.rerun()
        
        st.markdown("---")
        
        # Display agents as feature cards
        st.markdown("#### 📅 PlanerAgent")
        st.markdown("*Strategic content planning*")
        
        st.markdown("#### ✍️ RagWriterAgent") 
        st.markdown("*Content writing with references*")
        
        st.markdown("#### 🔍 SeoAgent")
        st.markdown("*SEO analysis & optimization*")
        
        st.markdown("#### 🔬 ResearchAgent")
        st.markdown("*Comprehensive topic research*")
    
    # Main content area
    show_chat_interface()