import os
import uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import werkzeug


try:
    account_url = "https://imagecaptioningstore.blob.core.windows.net"
    default_credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url=account_url, credential=default_credential)
    # Create a unique name for the container
    container_name = 'image-blobs'
    # Create the container, will skip if it already exists
    container_client = blob_service_client.create_container(container_name, public_access="blob")
except Exception as ex:
    print('Exception:')
    print(ex)


def upload_image_to_blob(image: werkzeug.datastructures.FileStorage):
    local_path = "../data"
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

    # delete the local file
    os.remove(upload_file_path)

    print("Url to the uploaded image: ", blob_client.url)
    return blob_client.url
