from pydantic import BaseModel, Field


class EmailInput(BaseModel):
    to: str
    subject: str
    body: str


class CalendarInput(BaseModel):
    title: str
    date: str
    time: str


class Route(BaseModel):
    destination: str = Field(
        description="send_email | create_calendar_event | fallback"
    )
