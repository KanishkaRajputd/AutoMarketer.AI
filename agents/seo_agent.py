import streamlit as st
from utils.get_llm_response import get_llm_response
from openai import OpenAI
from utils.get_llm_response import get_openai_client

def seo_agent(user_input):
    prompt = f"""
   You are an expert SEO assistant.

    Task: {user_input}

    Provide a concise, actionable SEO response. Focus your answer on:
    - Primary keyword(s) and search intent
    - Top 5 keyword suggestions OR a step-by-step strategy (as needed)
    - One practical recommendation to improve SEO for the query
    - 5 suitable hashtags relevant to the topic

    Use a clear bullet or numbered list. Do not add extra explanations or sections.
    """
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a SEO specialist. Create a comprehensive SEO plan based on the user's requirements."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content