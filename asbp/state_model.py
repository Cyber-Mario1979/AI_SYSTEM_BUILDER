from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TaskModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    order: int = Field(ge=1)
    title: str = Field(min_length=1)
    description: str | None = None
    owner: str | None = None
    duration: int | None = Field(default=None, ge=1)
    status: Literal["planned", "in_progress", "completed", "over_due"]
    dependencies: list[str] = Field(default_factory=list)


class StateModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project: str
    version: str
    status: Literal["not_started", "in_flight", "completed"]
    tasks: list[TaskModel] = Field(default_factory=list)
