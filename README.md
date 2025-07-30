# Flutter-Perplexity-FastAPI

A real-time AI-powered search and chat application that combines web search capabilities with intelligent response generation. This project provides both WebSocket and REST API endpoints for seamless integration with Flutter applications.

## Features

- **Real-time WebSocket Communication**: Live streaming responses for interactive chat experiences
- **Web Search Integration**: Powered by Tavily API for comprehensive web search results
- **AI-Powered Responses**: Uses Google Gemini 2.0 Flash for intelligent, context-aware responses
- **Source Relevance Sorting**: Intelligent ranking of search results using semantic similarity
- **Content Extraction**: Automatic extraction of relevant content from web pages
- **Dual API Endpoints**: Both WebSocket and REST API support for different use cases

## Architecture

The application follows a modular service-oriented architecture:

- **Search Service**: Handles web search using Tavily API and content extraction
- **Sort Source Service**: Ranks search results by relevance using semantic similarity
- **LLM Service**: Generates AI responses using Google Gemini
- **FastAPI Backend**: Provides WebSocket and REST endpoints

## Project Structure

```
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration and environment settings
├── services/              # Core business logic services
│   ├── search_service.py      # Web search and content extraction
│   ├── sort_source_service.py # Source relevance ranking
│   └── llm_service.py         # AI response generation
├── pydantic_models/       # Data models
│   └── chat_body.py           # Request/response schemas
├── venv/                  # Python virtual environment
└── .env                   # Environment variables (not tracked)
```

## Prerequisites

- Python 3.8+
- Tavily API key
- Google Gemini API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Flutter-Perplexity-FastAPI
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn python-dotenv pydantic-settings tavily-python trafilatura google-generativeai sentence-transformers numpy
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   TAVILY_API_KEY=your_tavily_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

### Starting the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

### API Endpoints

#### WebSocket Chat Endpoint
- **URL**: `ws://localhost:8000/ws/chat`
- **Method**: WebSocket
- **Description**: Real-time streaming chat with search and AI response generation

**Message Format**:
```json
{
  "query": "Your search query here"
}
```

**Response Format**:
```json
{
  "type": "search_result",
  "data": [...]
}
```
```json
{
  "type": "content",
  "data": "AI generated response chunk"
}
```

#### REST Chat Endpoint
- **URL**: `POST /chat`
- **Method**: POST
- **Description**: Synchronous chat with search and AI response generation

**Request Body**:
```json
{
  "query": "Your search query here"
}
```

**Response**: Complete AI-generated response based on web search results

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## How It Works

1. **Query Processing**: User sends a query through WebSocket or REST API
2. **Web Search**: Tavily API searches the web for relevant information
3. **Content Extraction**: Trafilatura extracts clean content from web pages
4. **Relevance Ranking**: Sentence transformers calculate semantic similarity and rank sources
5. **AI Response**: Google Gemini generates comprehensive responses using ranked sources
6. **Streaming**: Responses are streamed back to the client in real-time

## Configuration

The application uses environment variables for configuration:

- `TAVILY_API_KEY`: Your Tavily API key for web search functionality
- `GEMINI_API_KEY`: Your Google Gemini API key for AI response generation

## Development

### Adding New Services

1. Create a new service file in the `services/` directory
2. Implement the service logic
3. Import and initialize the service in `main.py`
4. Add any required configuration to `config.py`

### Extending Models

1. Add new Pydantic models in the `pydantic_models/` directory
2. Import and use them in your endpoints

## Error Handling

The application includes basic error handling for:
- API key validation
- Network request failures
- Content extraction errors
- WebSocket connection issues

## Security Considerations

- API keys are stored in environment variables
- Input validation using Pydantic models
- Error messages don't expose sensitive information

## Performance

- Asynchronous processing for better concurrency
- Streaming responses for real-time user experience
- Semantic similarity filtering to reduce irrelevant content
- Efficient content extraction and processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 