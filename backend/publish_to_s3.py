import boto3


import os.path


def publish_to_s3(local_image_path: str) -> str:
    """Upload an image to S3 and return the public URL."""
    s3_client = boto3.client("s3")
    object_path = f"public/{os.path.basename(local_image_path)}"
    bucket_name = "future-junk-images"
    s3_client.upload_file(local_image_path, bucket_name, object_path)

    return f"https://{bucket_name}.s3.us-west-2.amazonaws.com/{object_path}"