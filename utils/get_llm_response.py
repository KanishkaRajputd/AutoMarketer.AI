import streamlit as st
from openai import OpenAI

def get_openai_client():
    """
    Get OpenAI client with API key from Streamlit secrets.
    
    Returns:
        OpenAI: OpenAI client instance
    """
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {str(e)}")
        return None

def get_llm_response(prompt):
    """
    Get response from OpenAI LLM using the provided prompt.
    
    Args:
        prompt (str): The prompt to send to the LLM
        
    Returns:
        str: The LLM response or fallback response if API fails
    """
    client = get_openai_client()
    
    if client is None:
        print("OpenAI client is not available")
        # Fallback to keyword-based routing if OpenAI is not available
        return _fallback_routing(prompt)
    
    try:    
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            max_tokens=10,
            temperature=0
        )
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        st.error(f"Error getting LLM response: {str(e)}")
        # Fallback to keyword-based routing
        print("Fallback to keyword-based routing")
        return _fallback_routing(prompt)

def _fallback_routing(prompt):
    """
    Fallback keyword-based routing when OpenAI API is not available.
    
    Args:
        prompt (str): The routing prompt
        
    Returns:
        str: Assigned agent name
    """
    prompt_lower = prompt.lower()
    
    # Simple keyword-based routing
    if any(word in prompt_lower for word in ['write', 'draft', 'copy', 'post', 'tweet', 'content', 'rewrite', 'improve']):
        return "RagWriterAgent"
    elif any(word in prompt_lower for word in ['plan', 'calendar', 'schedule', 'campaign', 'strategy', 'days']):
        return "PlanerAgent"
    elif any(word in prompt_lower for word in ['seo', 'keyword', 'search', 'ranking', 'meta', 'title', 'description']):
        return "SeoAgent"
    elif any(word in prompt_lower for word in ['research', 'trend', 'competitor', 'topic', 'insight', 'data']):
        return "ResearchAgent"
    else:
        return "ResearchAgent"
