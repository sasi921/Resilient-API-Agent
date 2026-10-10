from pydantic import BaseModel, Field

class Attempt(BaseModel):
    number: int = Field(ge=1)
    ok: bool
    status_code: int | None = None
    error: str | None = None

class ToolResult(BaseModel):
    ok: bool
    data: dict | list | None = None
    attempts: list[Attempt]
    source: str
