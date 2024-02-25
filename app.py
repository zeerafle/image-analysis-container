import werkzeug
from flask import Flask, request

import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

import uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Set the values of your computer vision endpoint and computer vision key
# as environment variables:
try:
    endpoint = os.environ["VISION_ENDPOINT"]
    key = os.environ["VISION_KEY"]
except KeyError:
    print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
    print("Set them before running this sample.")
    exit()

# Create an Image Analysis client
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

try:
    print("Azure Blob Storage Python quickstart sample")
    account_url = "https://imagecaptioningstore.blob.core.windows.net"
    default_credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url=account_url, credential=default_credential)
    # Create a unique name for the container
    container_name = 'image-blobs'
    # Create the container, skip if it already exists
    container_client = blob_service_client.create_container(container_name, public_access="blob")
except Exception as ex:
    print('Exception:')
    print(ex)

app = Flask(__name__)


def upload_image_to_blob(image: werkzeug.datastructures.FileStorage):
    local_path = "./data"
    if not os.path.exists(local_path): os.mkdir(local_path)

    # Save the image to a local file
    local_file_name = f"image-{uuid.uuid4()}"
    upload_file_path = os.path.join(local_path, local_file_name)
    image.save(upload_file_path)

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)

    print("Url to the uploaded image: ", blob_client.url)
    return blob_client.url


@app.route('/', methods=['POST'])
def image_analysis():
    file = request.files['image']
    image_url = upload_image_to_blob(file)
    # Get a caption for the image. This will be a synchronous (blocking) call.
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=[VisualFeatures.CAPTION]
    )
    print("Image analysis results:")
    # Print caption results to the console
    print(" Caption:")
    if result.caption is not None:
        return result.caption.text


if __name__ == '__main__':
    app.run()
