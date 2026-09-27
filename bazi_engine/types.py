from dataclasses import dataclass
from enum import Enum


class Element(str, Enum):
	WOOD = "木"
	FIRE = "火"
	EARTH = "土"
	METAL = "金"
	WATER = "水"


class Polarity(str, Enum):
	YANG = "阳"
	YIN = "阴"


@dataclass(frozen=True)
class Stem:
	name: str
	element: Element
	polarity: Polarity


@dataclass(frozen=True)
class Branch:
	name: str
	element: Element
	polarity: Polarity
	hidden_stems: tuple[str, ...]


@dataclass(frozen=True)
class Pillar:
	stem: Stem
	branch: Branch
