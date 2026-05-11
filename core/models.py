from pydantic import BaseModel, Field


class SlideContent(BaseModel):
    header: str = Field(..., max_length=80)
    text: str = Field(..., max_length=1200)
    image_query: str = Field(..., max_length=80)


class PresentationContent(BaseModel):
    slides: list[SlideContent]
