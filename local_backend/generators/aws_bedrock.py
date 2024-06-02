import base64
from pprint import pprint
import uuid
from PIL import Image
from io import BytesIO
import json
import boto3
from botocore.errorfactory import ClientError

from ..core import Cost, ImageGeneratorABC, ImageResult, MetapromptHints


class InappropriatePromptError(Exception):
    """
    Raised when the image generation prompt is blocked by AWS content filters.

    See https://aws.amazon.com/machine-learning/responsible-ai/policy/ for more information.
    """

    def __init__(self, prompt: str):
        self.prompt = prompt

    def __str__(self):
        return f"AWS blocked the prompt: {self.prompt}"


class Titan(ImageGeneratorABC):
    """
    Image generator using the Titan model from Amazon Bedrock.

    Strengths:
    - Realistic images
    - Traditional art styles

    Weaknesses:
    - Struggles with abstract or creative prompts
    - The prompt limit is 512 characters
    - Struggles with extra detail in prompts
    """

    model_name = "Amazon Titan"
    hints = MetapromptHints(metaprompt_id="titan", max_chars=480)

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

        configuration = {
            "quality": quality,
            "height": res,
            "width": res,
            # Specifies how strongly the generated image should adhere to the prompt. Use a lower value to introduce more randomness in the generation. Ranges 1.0 to 10.0.
            "cfgScale": 9.0,
            "numberOfImages": 1,
        }

        body = json.dumps(
            {
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {
                    "text": prompt,
                    # Optional. This seems to help slightly but it's tough to tell
                    "negativeText": "graphical artifacts, distortions, unreadable text",
                },
                "imageGenerationConfig": configuration,
            }
        )

        try:
            response = self.client.invoke_model(
                body=body,
                modelId="amazon.titan-image-generator-v1",
                accept="application/json",
                contentType="application/json",
            )
        except ClientError as e:
            # convert errors to make error handling easier
            if "blocked by our content filters" in e.response["Error"]["Message"]:
                raise InappropriatePromptError(prompt) from e
            else:
                raise ValueError(e.response["Error"]["Message"]) from e

        response_body = json.loads(response.get("body").read())
        image = Image.open(BytesIO(base64.b64decode(response_body["images"][0])))

        image_filename = f"{str(uuid.uuid4())}.jpg"

        image_path = f"{self.local_cache_dir}/{image_filename}"
        image.save(image_path)

        return ImageResult(
            path=image_path,
            debug_info={
                "configuration": configuration,
            },
        )
