from utils.get_llm_response import get_openai_client
import streamlit as st


# prompt chaining pattern
def planner_agent(user_input):
    prompt = f"""
    You are a strategic content planning specialist. Based on the user's requirements, list only day-wise content topics with a brief description for each. 
    - Detect the number of days needed from the user request; if not specified, default to 2 days.
    - For each day, provide a maximum of 3 topics.
    - For each topic, include a brief description.
    - Do not include any other sections (no schedule, KPIs, audience, etc.).

    User Request: {user_input}   
    Format your response STRICTLY as follows:
    Day 1:
    - [Topic 1]: [Brief description]
    - [Topic 2]: [Brief description]
    - [Topic 3]: [Brief description]

    Day 2:
    - [Topic 1]: [Brief description]
    - [Topic 2]: [Brief description]
    - [Topic 3]: [Brief description]

    [Add more days only if the user specifically asks for more.]
    """

    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a strategic content planning specialist. Create a comprehensive content plan based on the user's requirements."},
            {"role": "user", "content": prompt}
        ]
    )

    st.text('rethinking...')
    
    critic_prompt = f"""
    You are a critic and clarity expert.

    Review the following content plan and improve its clarity, focus, and usefulness.  
    Make sure each day's entry is:
    - Clear and easy to understand
    - Free from jargon or vague language
    - Aligned with the product's core value
    - Distinct from other days (no repetition)

    If a day’s theme or objective is unclear, rewrite it.
    If the message is too generic, make it more specific and value-driven.
    Keep the output structure unchanged.

    CONTENT PLAN:
    {response.choices[0].message.content}
    ------------------------------------------------------------
    Format your response STRICTLY as follows:
    Day 1:
    - [Topic 1]: [Brief description]
    - [Topic 2]: [Brief description]
    - [Topic 3]: [Brief description]

    Day 2:
    - [Topic 1]: [Brief description]
    - [Topic 2]: [Brief description]
    - [Topic 3]: [Brief description]

    [Add more days only if the user specifically asks for more.]
    """
    critic_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a critic and clarity expert. Review the following content plan and improve its clarity, focus, and usefulness."},
            {"role": "user", "content": critic_prompt}
        ]
    )
    return critic_response.choices[0].message.content