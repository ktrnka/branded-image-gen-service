from typing import NamedTuple, Optional
from ..core import Cost

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
