import re
import streamlit as st
from utils.get_llm_response import get_openai_client
from utils.get_embeddings import get_embeddings
from utils.handle_chroma_db import get_chroma_collection
from utils.sanitize_collection_name import sanitize_collection_name

# rag used agent
def handle_rag_writer_agent(user_input, uploaded_files, n_results=2):
    """
    Query the knowledge base with a question and get AI response.
        
    Args:
        question (str): The question to ask
        selected_doc_indices (list): List of selected document indices
        uploaded_documents (list): List of uploaded documents
        n_results (int): Number of results to retrieve
            
    Returns:
        str or None: AI response or None if error
    """
    try:
        query_embedding = get_embeddings(user_input)
        all_documents = []
        for index in uploaded_files:
            collection_name = sanitize_collection_name(index['name'])
            collection = get_chroma_collection(collection_name)
            
            if not collection:
                continue
                
            # Query the collection
            collection_results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # Add the documents from this collection to our results
            if collection_results and 'documents' in collection_results:
                for doc_list in collection_results['documents']:
                    all_documents.extend(doc_list)
        
        # Get OpenAI client
        client = get_openai_client()
        if not client or not all_documents:
            return None
            
        # Combine all documents into context
        context = "\n\n".join(all_documents)  # Limit to top 10 most relevant chunks
            
        # Generate response using retrieved context
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": f"""You are an expert content writer. Using the following reference material: {context}
                
                Write a compelling post about: {user_input}

                **Guidelines:**
                - Leverage insights from the provided context
                - Create engaging, original content  
                - Use a conversational yet professional tone
                - Include relevant examples from the context
                - Structure with clear headings and formatting
                - Deliver actionable value to readers

                Write a complete, ready-to-publish post."""
            }]
        )
        
        return response.choices[0].message.content or None
        
    except Exception as e:
        st.error(f"Error querying knowledge base: {str(e)}")
        return None



def handle_rag_writer_agent_without_files(user_input):
    try:
        prompt = f"""
        You are an expert content writer who creates engaging, high-quality posts on any topic. 
        
        **Your Task:** Write a compelling post about: {user_input}
        
        **Writing Guidelines:**
        - Create original, engaging content that captures the reader's attention
        - Use a conversational yet professional tone
        - Include actionable insights when relevant  
        - Structure with clear headings and bullet points for readability
        - Add relevant examples or case studies if applicable
        - Keep content informative and value-driven
        - Optimize for engagement with compelling hooks and conclusions
        
        **Output:** Provide a complete, ready-to-publish post that delivers real value to readers."""
        
        # Generate response using OpenAI
        client = get_openai_client()
        if not client:
            return None
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        return response.choices[0].message.content or None
    except Exception as e:
        st.error(f"Error querying knowledge base: {str(e)}")
        return None

def rag_writer_agent(user_input, uploaded_files):
    response = None
    if uploaded_files:
        response = handle_rag_writer_agent(user_input, uploaded_files)
    else:
        response = handle_rag_writer_agent_without_files(user_input)

    return response or None
    
       