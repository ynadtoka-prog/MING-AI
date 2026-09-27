from datetime import datetime, timedelta

from .location import BirthLocation


def timezone_offset_at(
    local_moment: datetime,
    location: BirthLocation,
) -> timedelta:
    """Return the UTC offset at this moment in the birthplace timezone."""
    if local_moment.tzinfo is None:
        raise ValueError("local_moment must be timezone-aware")

    moment_in_location_timezone = local_moment.astimezone(location.timezone)
    offset = moment_in_location_timezone.utcoffset()
    if offset is None:
        raise ValueError("Unable to determine timezone UTC offset.")
    return offset


def standard_meridian(
    local_moment: datetime,
    location: BirthLocation,
) -> float:
    """Return the timezone meridian longitude in degrees."""
    offset = timezone_offset_at(local_moment, location)
    return offset.total_seconds() / 3600 * 15.0


def longitude_time_offset(
    local_moment: datetime,
    location: BirthLocation,
) -> timedelta:
    """Calculate mean-solar correction from longitude and timezone meridian."""
    if local_moment.tzinfo is None:
        raise ValueError("local_moment must be timezone-aware")

    meridian = standard_meridian(local_moment, location)
    longitude_difference = location.longitude - meridian
    return timedelta(minutes=longitude_difference * 4.0)


def mean_solar_time(
    local_moment: datetime,
    location: BirthLocation,
) -> datetime:
    """Convert local civil time to mean solar time (without Equation of Time)."""
    if local_moment.tzinfo is None:
        raise ValueError("local_moment must be timezone-aware")

    return local_moment + longitude_time_offset(local_moment, location)