from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Literal
from database import init_db, get_connection
from models import MovieCreate, MovieUpdate, MovieOut

app = FastAPI(
    title="Movie Collection API",
    description="A simple CRUD API for managing a movie collection, backed by SQLite.",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    init_db()


def row_to_movie(row) -> dict:
    return {
        "movie_id": row["movie_id"],
        "title": row["title"],
        "director": row["director"],
        "genre": row["genre"],
        "duration": row["duration"],
        "rating": row["rating"],
    }


@app.get("/movies", response_model=list[MovieOut], tags=["Movies"])
def get_movies():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM movies").fetchall()
    return [row_to_movie(r) for r in rows]


@app.get("/movies/sort", response_model=list[MovieOut], tags=["Movies"])
def sort_movies(
    sort_by: Literal["duration", "rating"] = Query(
        "rating", description="Field to sort by: duration or rating"
    ),
    order: Literal["asc", "desc"] = Query(
        "desc", description="Sort direction: asc or desc"
    ),
):

    direction = "ASC" if order == "asc" else "DESC"
    query = f"SELECT * FROM movies ORDER BY {sort_by} {direction}"

    with get_connection() as conn:
        rows = conn.execute(query).fetchall()
    return [row_to_movie(r) for r in rows]


@app.get("/movies/{movie_id}", response_model=MovieOut, tags=["Movies"])
def get_movie(movie_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM movies WHERE movie_id = ?", (movie_id,)
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404, detail=f"Movie with movie_id {movie_id} not found."
        )
    return row_to_movie(row)

@app.post(
    "/create_movies",
    response_model=MovieOut,
    status_code=201,
    tags=["Movies"],
)
def create_movie(movie: MovieCreate):
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT 1 FROM movies WHERE movie_id = ?", (movie.movie_id,)
        ).fetchone()

        if existing is not None:
            raise HTTPException(
                status_code=400,
                detail=f"A movie with movie_id {movie.movie_id} already exists.",
            )

        conn.execute(
            """
            INSERT INTO movies (movie_id, title, director, genre, duration, rating)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                movie.movie_id,
                movie.title,
                movie.director,
                movie.genre.value,
                movie.duration,
                movie.rating,
            ),
        )
        conn.commit()

    return movie.model_dump()

@app.put("/movies/{movie_id}", response_model=MovieOut, tags=["Movies"])
def update_movie(movie_id: int, movie: MovieUpdate):
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT 1 FROM movies WHERE movie_id = ?", (movie_id,)
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404, detail=f"Movie with movie_id {movie_id} not found."
            )

        conn.execute(
            """
            UPDATE movies
            SET title = ?, director = ?, genre = ?, duration = ?, rating = ?
            WHERE movie_id = ?
            """,
            (
                movie.title,
                movie.director,
                movie.genre.value,
                movie.duration,
                movie.rating,
                movie_id,
            ),
        )
        conn.commit()

    return {**movie.model_dump(), "movie_id": movie_id}


@app.delete("/movies/{movie_id}", tags=["Movies"])
def delete_movie(movie_id: int):
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT 1 FROM movies WHERE movie_id = ?", (movie_id,)
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404, detail=f"Movie with movie_id {movie_id} not found."
            )

        conn.execute("DELETE FROM movies WHERE movie_id = ?", (movie_id,))
        conn.commit()

    return JSONResponse(
        status_code=200,
        content={"message": f"Movie with movie_id {movie_id} was deleted successfully."},
    )