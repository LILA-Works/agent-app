from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, JsonValue, StringConstraints

type NodeId = str
type LogPath = Annotated[
    str, StringConstraints(pattern=r"^\$(\.[A-Za-z_][A-Za-z0-9_-]*(\[\d+\])*)+$")
]


class JsonSchema(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["object", "array", "string", "number", "integer", "boolean", "null"] | None = None
    description: str = ""
    properties: dict[str, "JsonSchema"] | None = None
    required: tuple[str, ...] = ()
    items: "JsonSchema | None" = None
    enum: tuple[JsonValue, ...] | None = None
