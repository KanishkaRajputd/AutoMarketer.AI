import streamlit as st
import time
from streamlit_extras.add_vertical_space import add_vertical_space
from utils.sanitize_collection_name import sanitize_collection_name
from utils.assign_agent import assign_agent
from interfaces.session_history import add_to_history, initialize_history, get_history
from utils.handle_agent_call import handle_agent_call
from utils.extract_pdf_content import extract_pdf_content, validate_pdf_file, get_pdf_metadata
from utils.handle_file_upload import handle_file_upload
from utils.handle_chroma_db import clear_chroma_db


def show_chat_interface():
    """Display a ChatGPT-style interface with conversation history and input at bottom"""
    
    # Initialize history
    initialize_history()
    
    # Initialize session state
    if "last_assigned_agent" not in st.session_state:
        st.session_state.last_assigned_agent = None
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    if "pending_agent_call" not in st.session_state:
        st.session_state.pending_agent_call = None
    if "pending_user_input" not in st.session_state:
        st.session_state.pending_user_input = None
    if "num_file_slots" not in st.session_state:
        st.session_state.num_file_slots = 1
    if "show_file_upload" not in st.session_state:
        st.session_state.show_file_upload = False
    if "processing_files" not in st.session_state:
        st.session_state.processing_files = []
    
    # Custom CSS for the simple interface
    st.markdown("""
    <style>
        .chat-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 1rem;
            height: calc(100vh - 200px);
            display: flex;
            flex-direction: column;
        }
        
        .chat-history {
            flex: 1;
            overflow-y: auto;
            padding: 1rem 0;
            margin-bottom: 2rem;
        }
        
        .user-message {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 15px 15px 5px 15px;
            margin: 1rem 0;
            margin-left: 20%;
            box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        }
        
        .agent-message {
            background: transparent;
            color: #fffff;
            padding: 1rem 1.5rem;
            border-radius: 15px 15px 15px 5px;
            margin: 1rem 0;
            margin-right: 20%;
            border-left: 4px solid #48bb78;
            box-shadow: none;
            font-size: 0.85rem;
            line-height: 1.4;
        }
        
        .agent-header {
            font-weight: 600;
            color: #667eea;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .empty-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 60%;
            text-align: center;
            color: #6b7280;
        }
        
        .empty-logo {
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #ffd700, #ffed4e, #fbbf24);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
        }
        
        .empty-subtitle {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            line-height: 1.6;
        }
        
        .example-prompts {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
            max-width: 800px;
        }
        
        .example-prompt {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: left;
        }
        
        .example-prompt:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-color: #667eea;
        }
        
        .input-container {
            background: white;
            border-radius: 25px;
            padding: 1rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
            margin-top: auto;
        }
        
        .input-container:focus-within {
            border-color: #667eea;
            box-shadow: 0 4px 25px rgba(102, 126, 234, 0.2);
        }
        
        .add-file-btn {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.9rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3);
        }
        
        .add-file-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
        }
        
        /* Remove default Streamlit padding */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        
        /* Custom scrollbar for chat history */
        .chat-history::-webkit-scrollbar {
            width: 6px;
        }
        
        .chat-history::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        .chat-history::-webkit-scrollbar-thumb {
            background: #c1c1c1;
            border-radius: 10px;
        }
        
        .chat-history::-webkit-scrollbar-thumb:hover {
            background: #a1a1a1;
        }
        
        /* Inline file uploader styles */
        .inline-uploader {
            background: #f8fafc;
            border: 2px dashed #e2e8f0;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            text-align: center;
        }
        
        .inline-uploader:hover {
            border-color: #667eea;
            background: #f1f5f9;
        }
        
        .file-item {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 0.75rem;
            margin: 0.5rem 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .file-remove-btn {
            background: #ef4444;
            color: white;
            border: none;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            cursor: pointer;
            font-size: 12px;
        }
        

    </style>
    """, unsafe_allow_html=True)
    
    # Chat history section
    history = get_history()
    st.markdown("""
        <div class="empty-state">
            <div class="empty-logo">AutoMarketer.AI</div>
        </div>
        """, unsafe_allow_html=True)  
  
    if not history:
        # Empty state with logo and examples
        st.markdown("""
        <div class="empty-state">
            <div class="empty-subtitle">
                How can I help you with your marketing needs today?<br>
                Choose an example below or type your own question.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display conversation history        
        for entry in history:
            # User message
            st.markdown(f"""
            <div class="user-message">
                {entry['query']}
            </div>
            """, unsafe_allow_html=True)
            
            # Agent response
            agent_emojis = {
                "PlanerAgent": "🗓️",
                "RagWriterAgent": "✍️", 
                "SeoAgent": "🔍",
                "ResearchAgent": "🔬"
            }
            emoji = agent_emojis.get(entry['agent_type'], "🤖")
            
            st.markdown(f"""
            <div class="agent-message">
                <div class="agent-header">
                    {emoji} {entry['agent_type']}
                </div>
                {entry['response']}
            </div>
            """, unsafe_allow_html=True)
            
    # Input container at bottom    
    # Show info message if RagWriterAgent is pending
    if st.session_state.pending_agent_call == "RagWriterAgent":
        st.info("💡 **If you want to upload a file you can upload by clicking on +AddFile button**")
        
        # Show inline file upload if activated
        if st.session_state.show_file_upload:
            st.markdown("**📁 Upload PDF Files**")
            
            # File uploader
            uploaded_files = st.file_uploader(
                "Choose PDF files",
                type=['pdf'],
                accept_multiple_files=True,
                help="Upload PDF files for analysis",
                key="inline_file_uploader"
            )
            
            # Process uploaded files immediately
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    # Check if file is already being processed or processed
                    if uploaded_file.name not in [f['name'] for f in st.session_state.processing_files] and \
                       uploaded_file.name not in [f['name'] for f in st.session_state.uploaded_files]:
                        
                        # Add to processing list
                        st.session_state.processing_files.append({
                            'name': uploaded_file.name,
                            'file': uploaded_file
                        })
                        
                        with st.spinner(f"Processing {uploaded_file.name}..."):
                            # Validate PDF
                            is_valid, error_message = validate_pdf_file(uploaded_file)
                            
                            if is_valid:
                                # Extract content
                                pdf_data = extract_pdf_content(uploaded_file)
                                
                                if not (pdf_data['content'].startswith("Error") or pdf_data['content'] == "No text content found in PDF"):
                                    # Add to knowledge base
                                    upload_success = handle_file_upload(pdf_data)
                                    
                                    if upload_success:
                                        # Add to session uploaded files
                                        doc_info = {
                                            'name': sanitize_collection_name(uploaded_file.name),
                                            'type': uploaded_file.type,
                                            'size': uploaded_file.size,
                                            'content': pdf_data['content'],
                                            'file_obj': uploaded_file,
                                            'upload_time': time.time()
                                        }
                                        st.session_state.uploaded_files.append(doc_info)
                                        uploaded_files=None
                                        st.success(f"✅ Successfully processed and added {uploaded_file.name}")
                                    else:
                                        st.error(f"❌ Failed to add {uploaded_file.name} to knowledge base")
                                else:
                                    st.error(f"❌ Could not extract content from {uploaded_file.name}")
                            else:
                                st.error(f"❌ Invalid PDF: {error_message}")

    # Input form
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "",
            placeholder="Type your message here...",
            height=100,
            key="chat_input",
            label_visibility="collapsed",
            value=st.session_state.pending_user_input if st.session_state.pending_user_input else ""
        )
        
        # Dynamic button layout based on pending agent
        if st.session_state.pending_agent_call == "RagWriterAgent":
            col1, col2, col3 = st.columns([1, 1, 6])
            with col1:
                # Send button with updated text
                file_count = len(st.session_state.uploaded_files)
                if file_count > 0:
                    send_text = f"Send with {file_count} file{'s' if file_count > 1 else ''}"
                else:
                    send_text = "Send without files"
                submitted = st.form_submit_button(send_text, use_container_width=True, type="primary")
            with col2:
                # Add File button
                add_file_clicked = st.form_submit_button("+ Add File", use_container_width=True)
        else:
            col1, col2, col3 = st.columns([1, 1, 6])
            with col1:
                submitted = st.form_submit_button("Send", use_container_width=True)
                add_file_clicked = False
               
        
    # Handle Add File button click
    if add_file_clicked:
        st.session_state.show_file_upload = not st.session_state.show_file_upload
        st.rerun()
        
    # Handle form submission
    if submitted and user_input.strip():
        # If there's a pending agent call (RagWriterAgent), execute it
        if st.session_state.pending_agent_call:
            with st.spinner("🤖 Processing your request..."):
                chat_response = handle_agent_call(
                    st.session_state.pending_agent_call, 
                    user_input,
                    st.session_state.uploaded_files
                )
            
            # Add to session history
            add_to_history(
                query=user_input,
                response=chat_response,
                agent_type=st.session_state.pending_agent_call
            )
            
            # Clear pending data and file upload state
            st.session_state.pending_agent_call = None
            st.session_state.pending_user_input = None
            st.session_state.show_file_upload = False
            
            # Rerun to show new message
            st.rerun()
        else:
            # Normal flow - assign agent and process
            with st.spinner("🤖 Assigning the best agent for your query..."):
                assigned_agent = assign_agent(user_input)
                st.session_state.last_assigned_agent = assigned_agent
                st.markdown(f"**💬 {assigned_agent} Response:**")
            
            # Check if RagWriterAgent is assigned
            if assigned_agent == "RagWriterAgent":
                st.session_state.pending_agent_call = assigned_agent
                st.session_state.pending_user_input = user_input
                st.rerun()
            else:
                # Get actual agent response for non-RAG agents
                with st.spinner("🤖 Processing your request..."):
                    chat_response = handle_agent_call(assigned_agent, user_input)
                
                # Add to session history
                add_to_history(
                    query=user_input,
                    response=chat_response,
                    agent_type=assigned_agent
                )
                
                # Rerun to show new message
                st.rerun()
    
    # Display uploaded files after the query box
    if st.session_state.uploaded_files:
        st.markdown("**📁 Uploaded Files:**")
        for i, file_info in enumerate(st.session_state.uploaded_files):
            col1, col2 = st.columns([10, 1])
            with col1:
                st.text(f"📄 {file_info['name']}")
            with col2:
                if st.button("✕", key=f"remove_uploaded_file_{i}", help="Remove file"):
                    clear_chroma_db(sanitize_collection_name(file_info['name']))
                    st.session_state.uploaded_files.pop(i)
                    st.rerun()


