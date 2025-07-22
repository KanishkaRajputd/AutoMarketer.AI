import streamlit as st
from interfaces.agents_interface import show_agents_interface
from interfaces.home_interface import show_home_interface

# Page configuration
st.set_page_config(
    page_title="AutoMarketer.AI - Intelligent Content Marketing Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)



def main():
    # Initialize session state
    if 'show_agents' not in st.session_state:
        st.session_state.show_agents = False
    
    # Check if we should show agents interface or home page
    if st.session_state.show_agents:
        show_agents_interface()
        return
    
    # Show home/landing page interface
    show_home_interface()

if __name__ == "__main__":
    main()
