from datetime import UTC, datetime, timedelta, tzinfo
from typing import TypedDict
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from lila.ext.tool import ToolError, tool

DISPLAY = "%Y-%m-%d %H:%M %Z"


class Now(TypedDict):
    """What ``now`` returns."""

    iso: str  # ISO 8601 with offset, in the resolved zone
    date: str  # YYYY-MM-DD
    time: str  # HH:MM:SS
    display: str  # preformatted for a message title, so no node has to assemble one
    timezone: str  # the resolved zone's name, e.g. ``PDT`` or ``Asia/Tokyo``
    utc_offset: str  # ``+09:00``
    iso_utc: str  # the same instant in UTC, so a record is never ambiguous


@tool
def now(timezone: str = "") -> Now:
    """The current date and time in one zone — an IANA name, or system local when empty.

    Raises:
        ToolError: the name is not a zone this machine knows.
    """
    moment = datetime.now(UTC)
    local = moment.astimezone(zone(timezone))
    return {
        "iso": local.isoformat(timespec="seconds"),
        "date": local.strftime("%Y-%m-%d"),
        "time": local.strftime("%H:%M:%S"),
        "display": local.strftime(DISPLAY).strip(),
        "timezone": timezone or local.tzname() or "",
        "utc_offset": _offset(local.utcoffset()),
        "iso_utc": moment.isoformat(timespec="seconds"),
    }


def zone(name: str) -> tzinfo:
    """One zone by IANA name, or this machine's when the name is empty.

    Raises:
        ToolError: the name is not a zone this machine knows.
    """
    if not name:
        local = datetime.now(UTC).astimezone().tzinfo
        return local if local is not None else UTC
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ToolError(f"unknown timezone {name!r}: {exc}") from exc


def _offset(delta: timedelta | None) -> str:
    """A UTC offset as ``+09:00``, or empty when there is none."""
    if delta is None:
        return ""
    minutes = int(delta.total_seconds() // 60)
    sign = "-" if minutes < 0 else "+"
    return f"{sign}{abs(minutes) // 60:02d}:{abs(minutes) % 60:02d}"
