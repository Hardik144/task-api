# Task API

A simple CRUD REST API built with FastAPI for the FlyRank Backend Assignment.

## Features

- Create tasks
- Read all tasks
- Read a single task
- Update a task
- Delete a task
- Health check endpoint
- Automatic Swagger documentation

## Tech Stack

- Python 3.14
- FastAPI
- Uvicorn

## Installation

```bash
git clone <repository-url>
cd task-api

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the project

```bash
uvicorn main:app --reload
```

Visit:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Welcome message |
| GET | /health | Health check |
| GET | /tasks | Get all tasks |
| GET | /tasks/{id} | Get one task |
| POST | /tasks | Create task |
| PUT | /tasks/{id} | Update task |
| DELETE | /tasks/{id} | Delete task |

## Sample Request

```json
{
  "title": "Learn FastAPI",
  "completed": false
}
```

## License

MIT