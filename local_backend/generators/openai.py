from urllib.parse import urlparse
from openai import OpenAI
import requests
from ..core import Cost, ImageGeneratorABC, ImageResult


class DallE(ImageGeneratorABC):
    """
    Image generator using the DALL-E 3 model from OpenAI API.

    Strengths:
    - Creative generation
    - Few artifacts
    - Long prompt length

    Weaknesses:
    - It can be expensive
    - It rewrites the prompt and often omits branding information
    """

    model_name = "OpenAI DALL-E 3"

    def __init__(self, local_cache_dir: str):
        self.local_cache_dir = local_cache_dir
        self.client = OpenAI()

    def generate(self, prompt: str, cost: Cost) -> ImageResult:
        configuration = dict(
            model="dall-e-3",
            size="1024x1024",
            quality="hd" if cost == Cost.HIGH else "standard",
        )
        response = self.client.images.generate(prompt=prompt, n=1, **configuration)

        response_data = response.data[0]
        response_url = response_data.url

        # Extract the filename from the URL
        parsed_url = urlparse(response_url)
        image_filename = parsed_url.path.split("/")[-1]

        image_path = f"{self.local_cache_dir}/{image_filename}"
        with open(image_path, "wb") as f:
            f.write(requests.get(response_url).content)

        return ImageResult(
            path=image_path,
            debug_info={
                "response": response_data.to_dict(),
                "configuration": configuration,
            },
        )
