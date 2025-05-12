# Streamlit Chatbot

A feature-rich chatbot application built with Streamlit that supports multiple LLM providers (OpenAI and Anthropic) with chat history persistence using PostgreSQL.

## Features

- Support for multiple LLM providers (OpenAI and Anthropic)
- Customizable base URL for OpenAI API (supports self-hosted models)
- Persistent chat history using PostgreSQL
- Session management with the ability to view and switch between chat sessions
- Model selection for each provider
- Modern and intuitive UI using Streamlit

## Prerequisites

- Docker and Docker Compose
- API keys for the LLM providers you want to use

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd chatbot
```

2. Create a `.env` file in the project root with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=your_openai_base_url  # Optional, for self-hosted models
ANTHROPIC_API_KEY=your_anthropic_api_key
```

3. Build and start the application:
```bash
docker-compose up --build
```

4. Access the application at `http://localhost:8501`

## Usage

1. Select your preferred LLM provider and model from the sidebar
2. Start a new chat session using the "New Chat" button
3. Type your message in the chat input and press Enter
4. View and switch between previous chat sessions from the sidebar
5. Each chat session maintains its own context and history

## Development

The project uses `uv` for dependency management. To add new dependencies:

1. Add them to `pyproject.toml`
2. Rebuild the Docker container:
```bash
docker-compose up --build
```

## Project Structure

```
chatbot/
├── app/
│   └── main.py           # Main Streamlit application
├── db/
│   └── models.py         # Database models
├── models/
│   ├── base.py          # Base model provider interface
│   ├── openai_provider.py
│   └── anthropic_provider.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Adding New Providers

To add a new LLM provider:

1. Create a new provider class in the `models` directory
2. Implement the `ModelProvider` interface
3. Add the provider to the `providers` dictionary in `app/main.py`

## License

MIT 