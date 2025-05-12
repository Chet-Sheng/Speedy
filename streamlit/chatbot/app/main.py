import streamlit as st
import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from db.models import ChatSession, ChatMessage, init_db
from models.openai_provider import OpenAIProvider
from models.anthropic_provider import AnthropicProvider

# Load environment variables
load_dotenv()

# Initialize database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/chatbot")
engine = init_db(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Initialize providers
providers = {
    "openai": OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        base_url=os.getenv("OPENAI_BASE_URL")
    ),
    "anthropic": AnthropicProvider(
        api_key=os.getenv("ANTHROPIC_API_KEY", "")
    )
}

def initialize_session_state():
    if "current_session" not in st.session_state:
        st.session_state.current_session = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_provider" not in st.session_state:
        st.session_state.selected_provider = "openai"
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = providers["openai"].get_available_models()[0]

def create_new_session():
    db_session = Session()
    new_session = ChatSession(
        title=f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        model_provider=st.session_state.selected_provider,
        model_name=st.session_state.selected_model
    )
    db_session.add(new_session)
    db_session.commit()
    st.session_state.current_session = new_session.id
    st.session_state.messages = []
    db_session.close()

def load_session(session_id):
    db_session = Session()
    session = db_session.query(ChatSession).get(session_id)
    if session:
        st.session_state.current_session = session.id
        st.session_state.messages = [
            {"role": msg.role, "content": msg.content}
            for msg in session.messages
        ]
        st.session_state.selected_provider = session.model_provider
        st.session_state.selected_model = session.model_name
    db_session.close()

def save_message(role, content):
    if st.session_state.current_session:
        db_session = Session()
        message = ChatMessage(
            session_id=st.session_state.current_session,
            role=role,
            content=content
        )
        db_session.add(message)
        db_session.commit()
        db_session.close()

def main():
    st.title("AI Chatbot")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar for session management and model selection
    with st.sidebar:
        st.header("Settings")
        
        # Provider selection
        provider = st.selectbox(
            "Select Provider",
            options=list(providers.keys()),
            index=list(providers.keys()).index(st.session_state.selected_provider)
        )
        st.session_state.selected_provider = provider
        
        # Model selection
        models = providers[provider].get_available_models()
        model = st.selectbox(
            "Select Model",
            options=models,
            index=models.index(st.session_state.selected_model)
        )
        st.session_state.selected_model = model
        
        # Session management
        st.header("Chat Sessions")
        db_session = Session()
        sessions = db_session.query(ChatSession).order_by(ChatSession.updated_at.desc()).all()
        
        if st.button("New Chat"):
            create_new_session()
        
        for session in sessions:
            if st.button(
                f"{session.title} ({session.model_name})",
                key=f"session_{session.id}"
            ):
                load_session(session.id)
        
        db_session.close()
    
    # Main chat interface
    if not st.session_state.current_session:
        st.info("Start a new chat from the sidebar!")
        return
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What's on your mind?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        save_message("user", prompt)
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = providers[st.session_state.selected_provider].chat_completion(
                    messages=st.session_state.messages,
                    model=st.session_state.selected_model
                )
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                save_message("assistant", response)

if __name__ == "__main__":
    main() 