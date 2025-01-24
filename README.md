# Book Tracker

A web application for managing your book collections across different lists like "Books I Own", "Books I've Read", and "Want to Read".

## Features

- Manage multiple book lists
- Track books across different categories
- User authentication
- Beautiful and responsive UI (coming soon with Svelte frontend)

## Backend Setup

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Run the backend server:
```bash
python app/main.py
```

The API will be available at http://localhost:8000

API Documentation is available at http://localhost:8000/docs

## Database

The application uses SQLite for data storage. The database file will be created automatically when you first run the application.

## Project Structure

```
book-tracker/
├── backend/
│   ├── app/
│   │   ├── database/
│   │   │   ├── database.py  # Database connection
│   │   │   └── models.py    # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic models
│   │   └── main.py         # FastAPI application
│   └── requirements.txt
└── frontend/               # Coming soon
```

## API Endpoints

- POST /books/ - Create a new book
- GET /books/ - List all books
- POST /lists/ - Create a new list
- GET /lists/{list_id} - Get a specific list
- POST /lists/{list_id}/books/{book_id} - Add a book to a list
