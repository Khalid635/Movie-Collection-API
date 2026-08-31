from enum import Enum
from pydantic import BaseModel, Field

class Genre(str, Enum):
    action = "action"
    comedy = "comedy"
    drama = "drama"
    thriller = "thriller"

class MovieCreate(BaseModel):
    movie_id: int = Field(..., description="Unique ID for the movie, becomes the primary key")
    title: str = Field(..., min_length=1, description="Title of the movie")
    director: str = Field(..., min_length=1, description="Director's name")
    genre: Genre = Field(..., description="One of: action, comedy, drama, thriller")
    duration: int = Field(..., gt=0, description="Runtime in minutes, must be positive")
    rating: float = Field(..., ge=0, le=5, description="Rating between 0 and 5 (inclusive)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "movie_id": 1,
                "title": "Inception",
                "director": "Christopher Nolan",
                "genre": "action",
                "duration": 148,
                "rating": 4.8,
            }
        }
    }

class MovieUpdate(BaseModel):
    title: str = Field(..., min_length=1, description="Title of the movie")
    director: str = Field(..., min_length=1, description="Director's name")
    genre: Genre = Field(..., description="One of: action, comedy, drama, thriller")
    duration: int = Field(..., gt=0, description="Runtime in minutes, must be positive")
    rating: float = Field(..., ge=0, le=5, description="Rating between 0 and 5 (inclusive)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Inception",
                "director": "Christopher Nolan",
                "genre": "action",
                "duration": 148,
                "rating": 4.9,
            }
        }
    }

class MovieOut(BaseModel):
    movie_id: int
    title: str
    director: str
    genre: Genre
    duration: int
    rating: float
