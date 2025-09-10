# Document Library Service

A FastAPI application that allows users to upload PDF documents, automatically processes them into pages/chunks, and provides APIs to manage and retrieve stored documents and their content.

## Live Demo

**API Base URL**: https://backend-amberflux-42819b9bb485.herokuapp.com  
**API Key**: `12345`  
**Interactive Docs**: https://backend-amberflux-42819b9bb485.herokuapp.com/docs


## Local Setup

### Prerequisites
- Python 3.9+
- PostgreSQL database
- pip

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd backend-fastapi-amberflux
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  -> on mac (I have used mac here)
source .venv\Scripts\activate -> on windows 
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
```bash
export DATABASE_URL="postgresql://admin:YKmcce3Pe9H4mgmBWOvzMPYqYBgjeNnq@dpg-d30adkvdiees73eshj60-a.oregon-postgres.render.com/document_library"
export API_KEY="12345"
export STORAGE_FOLDER="./storage"
export MAX_FILE_SIZE="10485760" 
export CHUNK_SIZE="800"
```

5. **Run the application**
```bash
uvicorn main:app --reload 
```

6. **Test the API:** -> using local host 


**Base URL**: `http://localhost:8000`  
**API Key**: `12345`

#### Health Check (No Auth Required)
```bash
curl -X GET "http://localhost:8000/health"
```

#### Root Endpoint (No Auth Required)
```bash
curl -X GET "http://localhost:8000/"
```

#### API Documentation (No Auth Required)
```bash
curl -X GET "http://localhost:8000/docs"
```

#### Upload Document (Query Auth)
```bash
curl -X POST "http://localhost:8000/documents?api_key=12345" \
  -F "file=@/path/to/your/document.pdf"
```

#### List All Documents (Query Auth)
```bash
curl -X GET "http://localhost:8000/documents?api_key=12345"
```

#### List Documents with Pagination (Query Auth)
```bash
curl -X GET "http://localhost:8000/documents?api_key=12345&limit=10&offset=0"
```

#### Get Document by ID (Query Auth)
```bash
curl -X GET "http://localhost:8000/documents/{document_id}?api_key=12345"
```

#### Get Document Page (Query Auth)
```bash
curl -X GET "http://localhost:8000/documents/{document_id}/pages/{page_number}?api_key=12345"
```

#### Search Documents (Query Auth)
```bash
curl -X GET "http://localhost:8000/search?q=your_search_term&api_key=12345"
```

#### Search with Custom Limit (Query Auth)
```bash
curl -X GET "http://localhost:8000/search?q=your_search_term&api_key=12345&limit=20"
```

#### Download Document (Query Auth)
```bash
curl -X GET "http://localhost:8000/documents/{document_id}/download?api_key=12345" \
  -o downloaded_document.pdf
```

#### Delete Document (Query Auth)
```bash
curl -X DELETE "http://localhost:8000/documents/{document_id}?api_key=12345"
```

### Health Check
```bash
curl -X GET "https://backend-amberflux-42819b9bb485.herokuapp.com/health"
```

### Upload Document
```bash
curl -X POST "https://backend-amberflux-42819b9bb485.herokuapp.com/documents?api_key=12345" \
  -F "file=@document.pdf"
```

### List Documents
```bash
curl -X GET "https://backend-amberflux-42819b9bb485.herokuapp.com/documents?api_key=12345"
```

### Get Document
```bash
curl -X GET "https://backend-amberflux-42819b9bb485.herokuapp.com/documents/{document_id}?api_key=12345"
```

### Get Document Page
```bash
curl -X GET "https://backend-amberflux-42819b9bb485.herokuapp.com/documents/{document_id}/pages/{page_number}?api_key=12345"
```

### Search Documents
```bash
curl -X GET "https://backend-amberflux-42819b9bb485.herokuapp.com/search?q=keyword&api_key=12345"
```

### Download Document
```bash
curl -X GET "https://backend-amberflux-42819b9bb485.herokuapp.com/documents/{document_id}/download?api_key=12345" \
  -o downloaded_document.pdf
```

### Delete Document
```bash
curl -X DELETE "https://backend-amberflux-42819b9bb485.herokuapp.com/documents/{document_id}?api_key=12345"
```

## Browser-Friendly URLs (Copy & Paste)

### Health Check
```
https://backend-amberflux-42819b9bb485.herokuapp.com/health
```

### Root Endpoint
```
https://backend-amberflux-42819b9bb485.herokuapp.com/
```

### API Documentation
```
https://backend-amberflux-42819b9bb485.herokuapp.com/docs
```

### List Documents
```
https://backend-amberflux-42819b9bb485.herokuapp.com/documents?api_key=12345
```

### Search Documents
```
https://backend-amberflux-42819b9bb485.herokuapp.com/search?q=your_search_term&api_key=12345
```

### Get Document (replace {document_id})
```
https://backend-amberflux-42819b9bb485.herokuapp.com/documents/{document_id}?api_key=12345
```

### Get Document Page (replace {document_id} and {page_number})
```
https://backend-amberflux-42819b9bb485.herokuapp.com/documents/{document_id}/pages/{page_number}?api_key=12345
```

### Download Document (replace {document_id})
```
https://backend-amberflux-42819b9bb485.herokuapp.com/documents/{document_id}/download?api_key=12345
```



## Features

- ✅ PDF document upload and storage
- ✅ Automatic text extraction and chunking
- ✅ Background processing for large files
- ✅ Document management (list, retrieve, delete)
- ✅ Page-by-page content access
- ✅ Keyword search across documents
- ✅ API key authentication
- ✅ File size limits and validation
- ✅ PostgreSQL database persistence
- ✅ Health monitoring

## Request/Response Formats

### Upload Response
```json
{
  "id": "uuid-string",
  "filename": "document.pdf",
  "size": 1024000,
  "page_count": 5,
  "status": "processing",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Document List Response
```json
{
  "documents": [
    {
      "id": "uuid-string",
      "filename": "document.pdf",
      "size": 1024000,
      "page_count": 5,
      "status": "ready",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

### Page Content Response
```json
{
  "page_number": 1,
  "text": "Page content here...",
  "chunks": [
    "Chunk 1 content...",
    "Chunk 2 content..."
  ]
}
```

### Search Response
```json
[
  {
    "document_id": "uuid-string",
    "document_filename": "document.pdf",
    "page_number": 1,
    "text_snippet": "Found text with keyword..."
  }
]
```

### Health Check Response
```json
{
  "status": "healthy",
  "fastapi_version": "0.116.1",
  "db_connection": true
}
```



## 🔧 Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://admin:YKmcce3Pe9H4mgmBWOvzMPYqYBgjeNnq@dpg-d30adkvdiees73eshj60-a.oregon-postgres.render.com/document_library` | Database connection string |
| `API_KEY` | `12345` | API key for authentication |
| `STORAGE_FOLDER` | `./storage` | Directory for storing uploaded files |
| `MAX_FILE_SIZE` | `10485760` | Maximum file size in bytes (10MB) |
| `CHUNK_SIZE` | `800` | Text chunk size for processing |


### API Key Issues

- **Local**: Default API key is `12345`
- **Production**: Check Heroku environment variables
- **Both header and query parameter authentication supported**

### File Upload Issues

- **File size limit**: 10MB maximum
- **File type**: Only PDF files allowed
- **Processing time**: Large files may take time to process

## Known Limitations

- Only supports PDF files
- Text extraction quality depends on PDF structure
- Large files may take time to process
- No image or table extraction
- Single API key for all users
- No user management system


## 📝 Notes

- **Replace `{document_id}`** with actual document IDs from your database
- **Replace `{page_number}`** with actual page numbers (1, 2, 3, etc.)
- **Replace `/path/to/your/document.pdf`** with actual file paths
- **Both authentication methods work** - choose header or query parameter based on your preference
- **Query parameter method** is easier for browser testing
- **Header method** is more secure for production use

