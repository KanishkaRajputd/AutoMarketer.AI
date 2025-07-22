from agents.planner_agent import planner_agent
from agents.rag_writer_agent import rag_writer_agent
from agents.seo_agent import seo_agent
from agents.research_agent import research_agent

def handle_agent_call(agent_name, user_input, uploaded_files=None):
    match agent_name:
        case "PlanerAgent":
            response = planner_agent(user_input)
            return response
        case "RagWriterAgent":
            return rag_writer_agent(user_input, uploaded_files)
        case "SeoAgent":
            return seo_agent(user_input)
        case "ResearchAgent":
            return research_agent(user_input)