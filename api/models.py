from pydantic import BaseModel


class User(BaseModel):
    login: str
    id: int
    created_at : str
    avatar_url : str
    bio : str