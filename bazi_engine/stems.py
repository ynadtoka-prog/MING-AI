from .types import Element, Polarity, Stem


STEMS: tuple[Stem, ...] = (
	Stem("甲", Element.WOOD, Polarity.YANG),
	Stem("乙", Element.WOOD, Polarity.YIN),
	Stem("丙", Element.FIRE, Polarity.YANG),
	Stem("丁", Element.FIRE, Polarity.YIN),
	Stem("戊", Element.EARTH, Polarity.YANG),
	Stem("己", Element.EARTH, Polarity.YIN),
	Stem("庚", Element.METAL, Polarity.YANG),
	Stem("辛", Element.METAL, Polarity.YIN),
	Stem("壬", Element.WATER, Polarity.YANG),
	Stem("癸", Element.WATER, Polarity.YIN),
)


STEM_BY_NAME: dict[str, Stem] = {
	stem.name: stem for stem in STEMS
}
