# Discord RAG Bot - Internship Assistant

A sophisticated Discord bot powered by **Retrieval-Augmented Generation (RAG)** that answers questions about the internship program using a knowledge base. The bot leverages advanced NLP embeddings, vector search, and a large language model to provide accurate, context-aware responses.

---

## 🌟 Features

- **📚 RAG Architecture**: Retrieves relevant context from a knowledge base before generating answers
- **🤖 Discord Integration**: Seamlessly responds to messages in Discord channels
- **💾 Multiple Document Support**: Ingests `.txt`, `.pdf`, and `.docx` files
- **🔄 Chat History**: Optional conversation history tracking with MongoDB
- **⚡ Fast Retrieval**: Vector-based semantic search using Pinecone
- **🧠 Advanced LLM**: Uses Groq's Llama 3.1 model for high-quality responses
- **💪 Scalable**: Containerized with Docker for easy deployment
- **🔐 Secure**: Sensitive credentials managed via environment variables

---

## 🏗️ Architecture

```
User Question
    ↓
[RAG Pipeline]
    ├── Retrieve Context (Pinecone Vector Search)
    ├── Get Chat History (MongoDB - optional)
    └── Build Prompt with System Instructions
    ↓
[LLM Processing]
    └── Groq (Llama 3.1 8B) Generates Response
    ↓
[Discord Bot]
    └── Send Response to User
    ↓
[Storage]
    ├── Store Chat History (MongoDB - optional)
    └── Embeddings Stored (Pinecone)
```

### Key Components

| Component               | Technology                           | Purpose                                           |
| ----------------------- | ------------------------------------ | ------------------------------------------------- |
| **Embeddings**          | Sentence Transformers (MiniLM-L6-v2) | Convert text to 384-dimensional vectors           |
| **Vector Database**     | Pinecone                             | Store and retrieve semantically similar documents |
| **Full-Text Database**  | MongoDB                              | Store raw document chunks and chat history        |
| **LLM**                 | Groq (Llama 3.1 8B)                  | Generate intelligent responses based on context   |
| **Chat Interface**      | Discord.py                           | Discord bot client for user interaction           |
| **Document Processing** | LangChain                            | Text splitting, document chunking, and utilities  |

---

## 📋 Prerequisites

- **Python 3.8+** (tested on 3.11)
- **API Keys** (required):
  - Discord Bot Token
  - Groq API Key
  - Pinecone API Key
- **Databases**:
  - Pinecone account (vector database)
  - MongoDB Atlas (or local MongoDB)
- **Docker** (optional, for containerization)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Anuj-k-45/Discord-RagBot.git
cd Discord-RagBot
```

### 2. Create Virtual Environment

```bash
# Create venv
python -m venv newVenv

# Activate venv
# On Windows:
newVenv\Scripts\activate
# On macOS/Linux:
source newVenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 1. Environment Variables (.env)

Create a `.env` file in the project root directory:

```env
# API Keys
GROQ_API_KEY=your_groq_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
TOKEN=your_discord_bot_token_here

# Optional: Chat History
ENABLE_CHAT_HISTORY=False
```

### 2. Obtain API Keys

#### Groq API Key

1. Visit [Groq Console](https://console.groq.com)
2. Sign up or log in
3. Generate an API key
4. Copy to `.env`

#### Pinecone API Key

1. Visit [Pinecone](https://www.pinecone.io)
2. Create a new project
3. Create an index named `rag-bot-v2` with:
   - **Dimension**: 384 (matches embedding model)
   - **Metric**: cosine (default)
4. Copy API key to `.env`

#### MongoDB Connection String

1. Visit [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster
3. Create a database user
4. Get the connection string
5. Copy to `.env`

#### Discord Bot Token

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the token to `.env`
5. Enable "Message Content Intent" under Privileged Gateway Intents

---

## 📖 Usage

### 1. Prepare Your Knowledge Base

Place documents in the `data/` folder:

```
data/
├── program_handbook.txt
├── internship_guide.pdf
└── company_policies.docx
```

Supported formats: `.txt`, `.pdf`, `.docx`

### 2. Ingest Documents

Run the ingestion script to process documents and populate the vector database:

```bash
python ingestion.py
```

Output:

```
🔄 Loading embedding model...
🔄 Connecting to Pinecone...
✅ Ingested 42 chunks successfully.
```

### 3. Start the Bot

```bash
python bot.py
```

Output:

```
🚀 Starting bot...
🔄 Loading embedding model...
🔄 Connecting to Pinecone...
🔄 Loading Groq LLM...
✅ Models loaded successfully
🤖 Bot is online and ready!
```

### 4. Interact in Discord

Simply mention the bot or send a message in a channel where it has access:

```
User: What's the internship duration?
Bot: The internship typically lasts 8-12 weeks...
```

---

## 📁 Project Structure

```
Discord-RagBot/
├── bot.py                    # Main Discord bot entry point
├── config.py                 # Configuration & environment variables
├── models.py                 # Initialize embedding model, Pinecone, and LLM
├── rag_pipeline.py          # Core RAG pipeline logic
├── ingestion.py             # Document loading and ingestion
├── chat_history.py          # MongoDB chat history management
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── .env                     # Environment variables (create this)
├── data/                    # Knowledge base documents
│   └── program_handbook.txt
├── newVenv/                 # Virtual environment (after setup)
└── __pycache__/            # Python cache files
```

### File Descriptions

| File               | Purpose                                                              |
| ------------------ | -------------------------------------------------------------------- |
| `bot.py`           | Entry point; handles Discord events and message routing              |
| `config.py`        | Centralized configuration; loads and validates environment variables |
| `models.py`        | Initializes all AI models (embedding, vector DB, LLM)                |
| `rag_pipeline.py`  | Core RAG logic: retrieves context and generates responses            |
| `ingestion.py`     | Processes documents; creates embeddings and stores in Pinecone       |
| `chat_history.py`  | Manages conversation history in MongoDB                              |
| `requirements.txt` | Lists all Python package dependencies                                |
| `Dockerfile`       | Container configuration for deployment                               |

---

## 🔄 How It Works

### Document Ingestion Flow

```
1. Load Documents (TXT, PDF, DOCX)
   ↓
2. Split into Chunks (500 chars, 100 overlap)
   ↓
3. Generate Embeddings (Sentence Transformers)
   ↓
4. Store Embeddings in Pinecone (vector search)
   ↓
5. Store Raw Chunks in MongoDB (retrieval)
```

### Query Processing Flow

```
1. User sends message in Discord
   ↓
2. Retrieve top-8 semantically similar chunks from Pinecone
   ↓
3. (Optional) Fetch recent chat history from MongoDB
   ↓
4. Build prompt with system instructions + context + history
   ↓
5. Send to Groq LLM (Llama 3.1 8B)
   ↓
6. Stream response back to Discord
   ↓
7. (Optional) Store conversation in MongoDB
```

### Vector Search Details

- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Dimension**: 384
- **Similarity Metric**: Cosine
- **Top-K Retrieved**: 8 chunks per query

---

## 🛠️ Technologies & Dependencies

### Core Libraries

| Library               | Version | Purpose                         |
| --------------------- | ------- | ------------------------------- |
| discord.py            | Latest  | Discord bot framework           |
| langchain             | Latest  | LLM orchestration & utilities   |
| langchain-groq        | Latest  | Groq provider for LangChain     |
| sentence-transformers | Latest  | Embedding model                 |
| pinecone-client       | Latest  | Vector database SDK             |
| pymongo               | Latest  | MongoDB driver                  |
| python-dotenv         | Latest  | Environment variable management |

### Document Processing

- **pypdf**: PDF text extraction
- **python-docx**: DOCX document processing
- **langchain_text_splitters**: Intelligent text chunking

### System

- **certifi**: SSL certificate verification
- **Python 3.8+**: Runtime

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t discord-ragbot .
```

### Run Container

```bash
docker run --env-file .env discord-ragbot
```

Make sure your `.env` file is in the same directory.

---

## 🔧 Configuration Options

### RAG Settings (in `config.py`)

```python
CHUNK_SIZE = 500           # Characters per chunk
CHUNK_OVERLAP = 100        # Overlap between chunks
DATA_PATH = "data"         # Directory with documents
TOP_K = 8                  # Retrieved chunks per query
ENABLE_CHAT_HISTORY = False # Enable MongoDB history
```

### LLM Settings

- **Model**: `llama-3.1-8b-instant` (via Groq)
- **Temperature**: 0 (deterministic responses)
- **Max Tokens**: 2000 characters (enforced in prompt)

### Embedding Model

- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimension**: 384
- **Normalized**: Yes (cosine similarity)

---

## ❓ Troubleshooting

### Issue: "API Key not found" Error

**Solution**: Ensure `.env` file exists and contains all required keys:

```bash
echo $env:GROQ_API_KEY  # Verify in PowerShell
```

### Issue: Bot Won't Connect to Discord

**Solution**:

1. Verify bot token is correct
2. Check bot has "Message Content Intent" enabled
3. Ensure bot is invited to the server with proper permissions

### Issue: Pinecone Connection Failed

**Solution**:

1. Verify API key and index name match
2. Check index has 384 dimensions
3. Ensure index is in the correct environment

### Issue: MongoDB Connection Timeout

**Solution**:

1. Check MONGODB_URI connection string
2. Verify IP is whitelisted in MongoDB Atlas
3. Ensure network connectivity

### Issue: Document Ingestion is Slow

**Solution**:

- Reduce `CHUNK_SIZE` or `CHUNK_OVERLAP` in `config.py`
- Process documents in batches
- Use fewer documents for testing

### Issue: Bot Responds with "I don't have that information"

**Solution**:

- Verify documents were ingested: `python ingestion.py`
- Check Pinecone index has vectors
- Ensure questions match document content semantically

---

## 📊 Performance Notes

- **Embedding Generation**: ~50-100ms per document
- **Vector Search**: ~100-200ms (Pinecone)
- **LLM Response**: ~500-2000ms (depends on context)
- **Total Response Time**: 1-3 seconds typical

---

## 🔐 Security Best Practices

✅ **Do This**:

- Store API keys in `.env` file
- Add `.env` to `.gitignore`
- Use environment variable substitution in Docker
- Enable SSL/TLS for MongoDB

❌ **Don't Do This**:

- Commit `.env` file to git
- Hardcode API keys in source code
- Log sensitive information
- Share API keys in repositories

---

## 📝 Environment Variables Reference

| Variable               | Required | Example                                  | Description                        |
| ---------------------- | -------- | ---------------------------------------- | ---------------------------------- |
| `GROQ_API_KEY`         | Yes      | `gsk_...`                                | Groq API authentication            |
| `PINECONE_API_KEY`     | Yes      | `pc_...`                                 | Pinecone vector DB key             |
| `MONGODB_URI`          | Yes      | `mongodb+srv://...`                      | MongoDB connection string          |
| `TOKEN`                | Yes      | `MTk4NjIyND...`                          | Discord bot token                  |
| `EMBEDDING_MODEL_NAME` | No       | `sentence-transformers/all-MiniLM-L6-v2` | Embedding model (default provided) |
| `LLM_MODEL_NAME`       | No       | `llama-3.1-8b-instant`                   | LLM model (default provided)       |
| `PINECONE_INDEX_NAME`  | No       | `rag-bot-v2`                             | Pinecone index name                |
| `ENABLE_CHAT_HISTORY`  | No       | `False`                                  | Enable MongoDB chat history        |
| `CHUNK_SIZE`           | No       | `500`                                    | Document chunk size                |
| `CHUNK_OVERLAP`        | No       | `100`                                    | Chunk overlap size                 |

---

## 🚀 Next Steps & Enhancements

- [ ] Add voice support for Discord
- [ ] Implement rate limiting
- [ ] Add user feedback mechanism
- [ ] Multi-language support
- [ ] Web dashboard for document management
- [ ] Advanced prompt tuning
- [ ] Caching for repeated queries
- [ ] Analytics and logging
- [ ] Unit tests and integration tests
- [ ] CI/CD pipeline with GitHub Actions

---

## 📄 License

This project is part of a programming assignment. Please review licensing requirements before using in production.

---

## 👤 Author

**Anuj K.**  
GitHub: [Anuj-k-45](https://github.com/Anuj-k-45)

---

## 📞 Support & Troubleshooting

For issues or questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review environment variable configuration
3. Check API service status
4. Review logs for error messages

---

## 📚 Additional Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Sentence Transformers](https://www.sbert.net/)
- [Groq API Documentation](https://console.groq.com/docs)
- [MongoDB Documentation](https://docs.mongodb.com/)

---

**Last Updated**: February 2026  
**Version**: 1.0.0
