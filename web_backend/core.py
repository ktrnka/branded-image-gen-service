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
    response_metadata: Optional[str]

    @property
    def filename(self) -> str:
        return self.path.split("/")[-1]


class ImageGeneratorABC:
    model_name: str
    prompt_max_chars: Optional[int] = None
    metaprompt_id = "default"

    def generate(self, prompt: str, cost: Cost) -> ImageResult:
        raise NotImplementedError(
            "generate method must be implemented in subclass. It should return a path to the generated image."
        )
