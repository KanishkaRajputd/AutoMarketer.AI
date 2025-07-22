import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

def show_home_interface():
    """Display the home/landing page interface"""
    
    # Custom CSS for beautiful styling
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .main-title {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #ffd700, #ffed4e, #fbbf24);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
        }
        
        .sub-title {
            font-size: 1.3rem;
            opacity: 0.9;
            margin-bottom: 2rem;
            line-height: 1.6;
        }
        
        .agent-card {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 1rem 0;
            border-left: 4px solid #667eea;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .agent-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .agent-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .agent-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #1a202c;
            margin-bottom: 0.5rem;
        }
        
        .agent-description {
            color: #4a5568;
            line-height: 1.6;
            margin-bottom: 1rem;
        }
        
        .feature-list {
            list-style: none;
            padding: 0;
        }
        
        .feature-list li {
            padding: 0.3rem 0;
            color: #2d3748;
        }
        
        .feature-list li:before {
            content: "✨";
            margin-right: 0.5rem;
        }
        
        .stats-container {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 2rem 0;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            display: block;
        }
        
        .stat-label {
            font-size: 1rem;
            opacity: 0.9;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero Section with integrated CTA
    st.markdown("""
    <div class="main-header">
        <div class="main-title">AutoMarketer.AI</div>
        <div class="sub-title">
            Transform Your Content Strategy with AI-Powered Marketing Intelligence<br>
            Four Specialized Agents Working Together to Supercharge Your Content Creation
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Prominent Get Started button with enhanced styling
    add_vertical_space(2)
    
    # Center the button with custom styling
    st.markdown("""
    <div style="display: flex; justify-content: center;">
        <style>
            .stButton > button {
                background: linear-gradient(135deg, #ff6b6b 0%, #feca57 50%, #48dbfb 100%) !important;
                color: white !important;
                font-size: 1.5rem !important;
                font-weight: 700 !important;
                padding: 1rem 3rem !important;
                border: none !important;
                border-radius: 50px !important;
                box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3) !important;
                transition: all 0.3s ease !important;
                text-transform: uppercase !important;
                letter-spacing: 1px !important;
                min-width: 300px !important;
            }
            .stButton > button:hover {
                transform: translateY(-3px) !important;
                box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4) !important;
                background: linear-gradient(135deg, #ff5252 0%, #ffc107 50%, #03a9f4 100%) !important;
            }
            .stButton > button:active {
                transform: translateY(-1px) !important;
            }
        </style>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Started Now - It's Free!", key="get_started_main", use_container_width=True):
            st.session_state.show_agents = True
            st.rerun()
    
    add_vertical_space(3)
    
    # Introduction
    st.markdown("### 🎯 **Meet Your AI Marketing Dream Team**")
    st.markdown("Harness the power of artificial intelligence with our suite of specialized agents designed to revolutionize your content marketing workflow.")
    
    add_vertical_space(2)
    
    # Agent Cards Section
    col1, col2 = st.columns(2)
    
    with col1:
        # Planer Agent
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">📅</div>
            <div class="agent-title">PlanerAgent</div>
            <div class="agent-description">
                Strategic content planning made effortless. Create comprehensive 1-5 day content plans 
                tailored to any topic with intelligent scheduling and optimization.
            </div>
            <ul class="feature-list">
                <li>Multi-day content calendar generation</li>
                <li>Topic-based content strategy</li>
                <li>Optimal posting schedule recommendations</li>
                <li>Content type diversification</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # SEO Agent
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">🔍</div>
            <div class="agent-title">SeoAgent</div>
            <div class="agent-description">
                Maximize your content's search visibility with advanced SEO analysis, 
                keyword intelligence, and performance optimization recommendations.
            </div>
            <ul class="feature-list">
                <li>Real-time SEO scoring</li>
                <li>Keyword density analysis</li>
                <li>Meta tag optimization</li>
                <li>Search ranking predictions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # RAG Writer Agent
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">✍️</div>
            <div class="agent-title">RagWriterAgent</div>
            <div class="agent-description">
                Intelligent content creation powered by your own resources. Upload documents, 
                links, and references to generate contextually accurate and engaging content.
            </div>
            <ul class="feature-list">
                <li>Document and link processing</li>
                <li>Context-aware content generation</li>
                <li>Style consistency maintenance</li>
                <li>Multi-format content support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Research Agent
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">🔬</div>
            <div class="agent-title">ResearchAgent</div>
            <div class="agent-description">
                Deep dive into any topic with comprehensive research capabilities. 
                Gather insights, trends, and data to fuel your content strategy.
            </div>
            <ul class="feature-list">
                <li>Comprehensive topic research</li>
                <li>Trend analysis and insights</li>
                <li>Competitor content analysis</li>
                <li>Data-driven recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    add_vertical_space(3)
    
    # Stats Section
    st.markdown("""
    <div class="stats-container">
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 200px; margin: 1rem;">
                <span class="stat-number">10X</span>
                <div class="stat-label">Faster Content Creation</div>
            </div>
            <div style="flex: 1; min-width: 200px; margin: 1rem;">
                <span class="stat-number">95%</span>
                <div class="stat-label">SEO Score Improvement</div>
            </div>
            <div style="flex: 1; min-width: 200px; margin: 1rem;">
                <span class="stat-number">4</span>
                <div class="stat-label">Specialized AI Agents</div>
            </div>
            <div style="flex: 1; min-width: 200px; margin: 1rem;">
                <span class="stat-number">24/7</span>
                <div class="stat-label">Intelligent Automation</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    add_vertical_space(2)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 2rem;">
        <h4>🚀 AutoMarketer.AI - Where Intelligence Meets Marketing</h4>
        <p>Empowering content creators with cutting-edge AI technology</p>
    </div>
    """, unsafe_allow_html=True) 