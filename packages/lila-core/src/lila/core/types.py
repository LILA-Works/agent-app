from typing import Literal

from pydantic import BaseModel, ConfigDict, JsonValue

type NodeId = str


class JsonSchema(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["object", "array", "string", "number", "integer", "boolean", "null"] | None = None
    description: str = ""
    properties: dict[str, "JsonSchema"] | None = None
    required: tuple[str, ...] = ()
    items: "JsonSchema | None" = None
    enum: tuple[JsonValue, ...] | None = None
