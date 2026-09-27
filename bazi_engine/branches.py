from .types import Branch, Element, Polarity


BRANCHES: tuple[Branch, ...] = (
    Branch("子", Element.WATER, Polarity.YANG, ("癸",)),
    Branch("丑", Element.EARTH, Polarity.YIN, ("己", "癸", "辛")),
    Branch("寅", Element.WOOD, Polarity.YANG, ("甲", "丙", "戊")),
    Branch("卯", Element.WOOD, Polarity.YIN, ("乙",)),
    Branch("辰", Element.EARTH, Polarity.YANG, ("戊", "乙", "癸")),
    Branch("巳", Element.FIRE, Polarity.YIN, ("丙", "戊", "庚")),
    Branch("午", Element.FIRE, Polarity.YANG, ("丁", "己")),
    Branch("未", Element.EARTH, Polarity.YIN, ("己", "丁", "乙")),
    Branch("申", Element.METAL, Polarity.YANG, ("庚", "壬", "戊")),
    Branch("酉", Element.METAL, Polarity.YIN, ("辛",)),
    Branch("戌", Element.EARTH, Polarity.YANG, ("戊", "辛", "丁")),
    Branch("亥", Element.WATER, Polarity.YIN, ("壬", "甲")),
)


BRANCH_BY_NAME: dict[str, Branch] = {
    branch.name: branch for branch in BRANCHES
}