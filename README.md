# Custom WSGI Micro-Framework

A lightweight, zero-dependency Python web application framework built on top of PEP 3333 (WSGI specification).

## Features
- Modular route handler architecture
- Dynamic path dispatching with custom fallback (404) handling
- Built-in JSON serialization and header management
- Native compliance with Python standard library `wsgiref` server

## Architecture Overview
The application separates concerns into three distinct layers:
1. **WSGI Server Interface**: Handles raw socket communication and populates the CGI environment (`environ`).
2. **Router & Pipeline**: Resolves requested `PATH_INFO` against registered route handlers, serializes Python dictionaries to UTF-8 encoded JSON bytes, and sets mandatory HTTP response headers (`Content-Type`, `Content-Length`).
3. **Route Handlers**: Isolated business logic functions returning status codes and response dictionaries.

## Getting Started
Run the application using Python standard library:
```bash
python app.py

curl http://localhost:8888/
curl http://localhost:8888/health