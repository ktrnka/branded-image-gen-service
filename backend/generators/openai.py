from urllib.parse import urlparse
from openai import OpenAI
import requests
from .base import ImageGeneratorABC, ImageResult

class DallE(ImageGeneratorABC):
    model_name = "OpenAI DALL-E 3"

    def __init__(self, local_cache_dir: str):
        self.local_cache_dir = local_cache_dir
        self.client = OpenAI()

    def generate(self, prompt: str) -> ImageResult:
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        response_data = response.data[0]
        response_url = response_data.url

        # Extract the filename from the URL
        parsed_url = urlparse(response_url)
        image_filename = parsed_url.path.split("/")[-1]

        image_path = f"{self.local_cache_dir}/{image_filename}"
        with open(image_path, "wb") as f:
            f.write(requests.get(response_url).content)
        
        return ImageResult(path=image_path, response_metadata=response_data.to_json())
