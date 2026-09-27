from dataclasses import dataclass
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class BirthLocation:
	city: str
	latitude: float
	longitude: float
	timezone_name: str

	def __post_init__(self):
		if not -90 <= self.latitude <= 90:
			raise ValueError("Latitude must be between -90 and 90")

		if not -180 <= self.longitude <= 180:
			raise ValueError("Longitude must be between -180 and 180")

		if not self.city.strip():
			raise ValueError("City cannot be empty")

		ZoneInfo(self.timezone_name)

	@property
	def timezone(self) -> ZoneInfo:
		return ZoneInfo(self.timezone_name)
