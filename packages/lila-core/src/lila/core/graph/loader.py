from pathlib import Path

import yaml
from lila.core.graph.base import Graph
from lila.core.graph.errors import ParseError
from pydantic import ValidationError


def from_yaml(yaml_path: Path | str) -> Graph:
    """Given a path to YAML file, parse it into a graph object."""
    path = Path(yaml_path)

    try:
        raw = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        raise ParseError(f"invalid YAML in {path}: {e}") from e

    if not isinstance(raw, dict):
        raise ParseError(f"{path}: top level must be a mapping, got {type(raw).__name__}.")

    try:
        return Graph.model_validate({**raw, "source": yaml_path})
    except ValidationError as e:
        raise ParseError(_format_validation_error(e)) from e


# region: helpers
def _format_validation_error(e: ValidationError) -> str:
    """Parses the cryptic Pydantic validation errors into something more human-readable."""
    lines = []
    for err in e.errors():
        loc = ".".join(str(p) for p in err["loc"]) or "<root>"
        msg = err["msg"].removeprefix("Value error, ")
        lines.append(f"{loc}: {msg}")
    return "\n".join(lines)


# endregion helpers
