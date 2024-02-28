import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

try:
    endpoint = os.environ["COGNITIVE_SERVICE_ENDPOINT"]
    key = os.environ["COGNITIVE_SERVICE_KEY"]
    region = os.environ["COGNITIVE_SERVICE_REGION"]
except KeyError:
    print("Missing environment variable 'COGNITIVE_SERVICE_ENDPOINT' or 'COGNITIVE_SERVICE_KEY' or 'COGNITIVE_SERVICE_REGION'.")
    exit()

# Create an Image Analysis client
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)


def analyze_image(image_url: str):
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=[VisualFeatures.CAPTION]
    )

    return result.caption.text if result.caption is not None else None