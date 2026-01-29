from pydantic import BaseModel, Field


class EmailInput(BaseModel):
    to: str = Field(description="Adresse email du destinataire")
    subject: str = Field(description="Sujet de l'email")
    body: str = Field(description="Corps du message")


class CalendarInput(BaseModel):
    title: str
    date: str
    time: str


class Route(BaseModel):
    destination: str = Field(
        description="send_email | create_calendar_event | fallback"
    )
