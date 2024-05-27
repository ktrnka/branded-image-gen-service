from typing import NamedTuple, Optional

class ImageResult(NamedTuple):
    path: str
    response_metadata: Optional[str]

    @property
    def filename(self) -> str:
        return self.path.split("/")[-1]

class ImageGeneratorABC:
    model_name: str

    def generate(self, prompt: str) -> ImageResult:
        raise NotImplementedError("generate method must be implemented in subclass. It should return a path to the generated image.")