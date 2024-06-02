from dataclasses import dataclass
from enum import Enum
from typing import Optional, NamedTuple

class Cost(Enum):
    """
    Cost settings so that we can iteratively develop with low cost settings and release with higher cost settings
    """
    HIGH = 'HIGH'
    LOW = 'LOW'


@dataclass
class Brand:
    """
    Convenience wrapper around brand data
    """
    name: str
    market: str
    brand_identity: str
    brand_style: Optional[str] = None


class ImageResult(NamedTuple):
    path: str
    debug_info: Optional[dict]

    @property
    def filename(self) -> str:
        return self.path.split("/")[-1]

class MetapromptHints(NamedTuple):
    """
    Image generation engine hints for the metaprompt engine
    """
    metaprompt_id: str
    max_chars: Optional[int] = None

class ImageGeneratorABC:
    model_name: str
    hints: MetapromptHints = MetapromptHints(metaprompt_id="default")

    def generate(self, prompt: str, cost: Cost) -> ImageResult:
        raise NotImplementedError(
            "generate method must be implemented in subclass. It should return a path to the generated image."
        )
