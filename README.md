# Log Analyzer

A web application for analyzing log files with filtering capabilities and visual analytics.

## Features

- Upload and parse log files
- Filter logs by level and timestamp
- Visual analytics with charts
- Persistent storage of log data
- Docker containerization

## Setup and Running

### Using Docker (Recommended)

1. Build and run the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. Access the application at http://localhost:5000

### Manual Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python run.py
   ```

## Log File Format

The application expects log files in the following format:
```
YYYY-MM-DD HH:MM:SS LEVEL Message
```

Example:
```
2023-04-18 10:30:45 INFO Application started successfully
2023-04-18 10:30:46 ERROR Failed to connect to database
```

## Features

1. **File Upload**: Upload log files through the web interface
2. **Filtering**: Filter logs by:
   - Log level (INFO, WARNING, ERROR, DEBUG)
   - Date range
3. **Visualization**:
   - Log level distribution pie chart
   - Timeline of log entries
4. **Persistent Storage**: All parsed logs are stored in SQLite database

# Note: The following files and folders are not used in the current Streamlit-based project and can be removed for cleanup:
# - app/ (Flask backend, models, routes, templates, static)
# - run.py (Flask launcher)
# - instance/ (Flask instance folder, if present)
# - logs.db in app/ (duplicate db)
# - __pycache__/ (Python cache)
# - venv/ (local Python virtual environment, not needed in Docker)

# Only keep:
# - streamlit_app.py
# - requirements.txt
# - Dockerfile
# - docker-compose.yml
# - uploaded_logs/
# - sample.log
# - .streamlit/
# - logs.db (main db)

# To remove unused files, run:
# rm -rf app run.py instance __pycache__ venv
# rm -f app/logs.db
