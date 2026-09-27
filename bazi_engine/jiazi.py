from dataclasses import dataclass

from .stems import STEMS
from .branches import BRANCHES
from .types import Stem, Branch


@dataclass(frozen=True)
class JiaZi:
    index: int
    stem: Stem
    branch: Branch

    @property
    def name(self) -> str:
        return f"{self.stem.name}{self.branch.name}"


JIAZI_CYCLE: tuple[JiaZi, ...] = tuple(
    JiaZi(
        index=i,
        stem=STEMS[i % 10],
        branch=BRANCHES[i % 12],
    )
    for i in range(60)
)


JIAZI_BY_NAME: dict[str, JiaZi] = {
    jiazi.name: jiazi for jiazi in JIAZI_CYCLE
}