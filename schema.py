from pydantic import BaseModel, HttpUrl



class Image(BaseModel):
    url: HttpUrl
    name: str

class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: int | None = None
    email: str | None = None
    photo: Image | None = None

