import base64
from pprint import pprint
from PIL import Image
from io import BytesIO
import json
import boto3

bedrock_client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")

def generate_image(prompt: str):
    body = json.dumps(
        {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": prompt,   # Required
    #           "negativeText": "<text>"  # Optional
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,   # Range: 1 to 5 
                "quality": "premium",  # Options: standard or premium
                "height": 1024,         # Supported height list in the docs 
                "width": 1024,         # Supported width list in the docs
                # Specifies how strongly the generated image should adhere to the prompt. Use a lower value to introduce more randomness in the generation
                "cfgScale": 9.5,       # Range: 1.0 (exclusive) to 10.0
                # "seed": 42             # Range: 0 to 214783647
            }
        }
    )

    response = bedrock_client.invoke_model(
        body=body, 
        modelId="amazon.titan-image-generator-v1",
        accept="application/json", 
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())

    print("Bedrock response:")
    pprint(response_body)

    return Image.open(BytesIO(base64.b64decode(response_body["images"][0])))
