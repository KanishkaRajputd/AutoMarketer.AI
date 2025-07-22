from utils.get_llm_response import get_openai_client
from tavily import TavilyClient
import streamlit as st
import json


# tool user pattern
tools_to_use  = [   {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Getting updated info from web",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The topic or question to search"
                }
            },
            "required": ["query"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

def get_tavily_client():
    api_key = st.secrets["TAVILY_API_KEY"]
    tavilyClient = TavilyClient(api_key)
    return tavilyClient


def web_search(query):
    
  content = ""
  tavilyClient = get_tavily_client()
  response = tavilyClient.search(query=query,max_results=2)
  web_results = response.get("results")
  for r in web_results:
    content+=(r["content"])
  return (content)

def research_agent(user_input):
    prompt = f"""
    You are a ResearchAgent.

    Given the product or service description below, identify up to 5 relevant insights to inform marketing strategy or content planning.

    USER INPUT:  
    {user_input}

    For each insight, provide:
    - Insight: [short title or key point]
    - Category: [e.g., audience pain point, trending topic, competitor angle, content gap]
    - Why it matters: [1–2 lines]

    Return in plain text, formatted like this:

    Insight: [title]  
    Category: [type]  
    Why it matters: [explanation]  
    """

    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        tools = tools_to_use
        
    )
    tool_calls = response.choices[0].message.tool_calls
    tool_calls_id = tool_calls[0].id
    function_name = tool_calls[0].function.name
    arguments = json.loads(tool_calls[0].function.arguments)
    res = web_search(arguments.get("query"))

    final_reponse = client.chat.completions.create(
    model="gpt-4",
    messages=[{
        "role":"user","content": prompt
    },{
        "role":"assistant","tool_calls":tool_calls
    },
      {
        "role":"tool",
        "tool_call_id":tool_calls_id,
        "name":function_name,
        "content":res
    }]
    )

    return final_reponse.choices[0].message.content