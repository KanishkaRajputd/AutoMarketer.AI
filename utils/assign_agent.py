from .get_llm_response import get_llm_response

def assign_agent(user_input):
    """
    Assigns the most appropriate agent based on user input using routing logic.
    
    Args:
        user_input (str): The user's query or request
        
    Returns:
        str: The assigned agent name (PlanerAgent, RagWriterAgent, SeoAgent, or ResearchAgent)
    """
    
    routing_prompt = f"""
You are a strict routing assistant.

GOAL: Given the raw user prompt, select EXACTLY ONE best-matching agent from the fixed list below.

AVAILABLE AGENTS (DO NOT RENAME, DO NOT ADD):
 - PlanerAgent      (For planning, schedules, calendars, content plans, timelines)
 - RagWriterAgent   (For writing, drafting, content generation, especially if 'Rag' is the main subject)
 - SeoAgent         (For SEO optimization, keyword strategy, SERP/ranking related questions)
 - ResearchAgent    (For researching, looking up, fact finding, gathering information)

IMPORTANT:
- Focus on what the user wants to DO (the action or intention), not just the keywords or topics.
- If the prompt asks to PLAN something, always choose PlanerAgent, even if other agent names or their topics are mentioned.
- Do NOT select RagWriterAgent unless the user clearly asks you to WRITE, GENERATE, or DRAFT content, or if the main action is writing, not planning.
- DO NOT select an agent based solely on the mention of its name or related topic.
- Only respond with the agent name from the list above. NO extra text, NO explanations.

EXAMPLES:
1. User: "Plan 3days content on Rag"          → PlanerAgent
2. User: "Write a blog post about Rag"         → RagWriterAgent
3. User: "Best keywords for travel blog"       → SeoAgent
4. User: "Research top AI tools in 2024"      → ResearchAgent

User prompt : {user_input}
"""
    
    return get_llm_response(routing_prompt)



