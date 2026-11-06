# Movie Collection API

A REST API for managing a personal movie collection. Built with FastAPI and SQLite.

## Features

- Full movie CRUD — add, list, view, update and delete movies
- Sort movies by rating or duration, ascending or descending
- Validated data with Pydantic v2: genre (`action` / `comedy` / `drama` / `thriller`), rating 0–5, positive duration
- SQLite storage, created automatically on startup

## Tech stack

FastAPI, Uvicorn, Pydantic v2, SQLite (Python standard library)

## API overview

| Method | Path | Description |
|---|---|---|
| GET | `/movies` | List all movies |
| GET | `/movies/sort?sort_by=rating&order=desc` | List movies sorted by `rating` or `duration`, `asc` or `desc` |
| GET | `/movies/{movie_id}` | Get one movie |
| POST | `/movies` | Add a movie |
| PUT | `/movies/{movie_id}` | Update a movie |
| DELETE | `/movies/{movie_id}` | Delete a movie |

Interactive docs: http://127.0.0.1:8000/docs

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate        # on Windows Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Example

```bash
curl -X POST http://127.0.0.1:8000/movies \
  -H "Content-Type: application/json" \
  -d '{"movie_id": 1, "title": "Inception", "director": "Christopher Nolan", "genre": "action", "duration": 148, "rating": 4.8}'
```

## Author

**Khalid Bin Masud**

[GitHub](https://github.com/Khalid635) · [LinkedIn](https://www.linkedin.com/in/khalid-bin-masud-817a913b9)
