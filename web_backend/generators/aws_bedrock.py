import base64
from pprint import pprint
import uuid
from PIL import Image
from io import BytesIO
import json
import boto3
from botocore.errorfactory import ClientError

from .base import ImageGeneratorABC, ImageResult
from ..core import Cost

bedrock_client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")

class InappropriatePromptError(Exception):
    """
    Raised when the prompt is blocked by AWS content filters.
    """
    def __init__(self, prompt: str):
        self.prompt = prompt

    def __str__(self):
        return f"AWS blocked the prompt: {self.prompt}"


class Titan(ImageGeneratorABC):
    model_name = "Amazon Titan"
    prompt_max_chars = 480
    metaprompt_id = "titan"

    def __init__(self, local_cache_dir: str):
        self.local_cache_dir = local_cache_dir
        self.client = boto3.client(
            service_name="bedrock-runtime", region_name="us-west-2"
        )

    def generate(self, prompt: str, cost: Cost) -> ImageResult:
        match cost:
            case Cost.LOW:
                quality = "standard"
                res = 512
            case Cost.HIGH:
                quality = "premium"
                res = 1024
            case _:
                raise ValueError(f"Unknown cost: {cost}")

        body = json.dumps(
            {
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {
                    "text": prompt,  # Required
                    "negativeText": "graphical artifacts, distortions, unreadable text",  # Optional
                },
                "imageGenerationConfig": {
                    "numberOfImages": 1,  # Range: 1 to 5
                    "quality": quality,  # Options: standard or premium
                    "height": res,  # Supported height list in the docs
                    "width": res,  # Supported width list in the docs
                    # Specifies how strongly the generated image should adhere to the prompt. Use a lower value to introduce more randomness in the generation
                    "cfgScale": 9.0,  # Range: 1.0 (exclusive) to 10.0
                },
            }
        )

        try:
            response = bedrock_client.invoke_model(
                body=body,
                modelId="amazon.titan-image-generator-v1",
                accept="application/json",
                contentType="application/json",
            )
        except ClientError as e:
            if "blocked by our content filters" in e.response["Error"]["Message"]:
                raise InappropriatePromptError(prompt) from e
            else:
                raise ValueError(e.response["Error"]["Message"]) from e

        response_body = json.loads(response.get("body").read())
        image = Image.open(BytesIO(base64.b64decode(response_body["images"][0])))

        image_filename = f"{str(uuid.uuid4())}.jpg"

        image_path = f"{self.local_cache_dir}/{image_filename}"
        image.save(image_path)

        return ImageResult(path=image_path, response_metadata=None)
