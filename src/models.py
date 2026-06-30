from pydantic import BaseModel, Field
from typing import List, Optional

class TutorResponse(BaseModel):
    is_on_topic: bool = Field(..., description="True only if question matches selected topic")
    diagnosis: Optional[str] = Field(None, description="What the user might be misunderstanding")
    answer: str = Field(..., description="Clear, step-by-step explanation")
    code_example: Optional[str] = Field(None, description="Minimal, runnable code if applicable")
    best_practice_tip: Optional[str] = Field(None, description="One key tip or warning")
    references: List[str] = Field(default_factory=list, description="Official docs or authoritative sources")
