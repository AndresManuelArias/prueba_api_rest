from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Nombre del usuario"
    )

    email: EmailStr = Field(
        ...,
        max_length=100,
        description="Correo electrónico válido"
    )

    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Contraseña del usuario"
    )


class UserResponse(BaseModel):

    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True