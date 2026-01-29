from pydantic import BaseModel, Field


class EmailInput(BaseModel):
    to: str = Field(description="Adresse email du destinataire")
    subject: str = Field(description="Sujet de l'email")
    body: str = Field(description="Corps du message")
