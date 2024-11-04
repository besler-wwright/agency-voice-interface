# src/voice_assistant/models.py
from enum import Enum

from pydantic import BaseModel


class ModelName(Enum):
    """Enum for OpenAI model names"""

    BASE_MODEL = "gpt-4-1106-preview"
    FAST_MODEL = "gpt-4o-mini"


class WebUrl(BaseModel):
    url: str


class CreateFileResponse(BaseModel):
    """Response model for file creation"""

    file_name: str
    file_content: str


class FileSelectionResponse(BaseModel):
    file: str
    model: ModelName = ModelName.BASE_MODEL


class FileUpdateResponse(BaseModel):
    updates: str


class FileDeleteResponse(BaseModel):
    file: str
    force_delete: bool
