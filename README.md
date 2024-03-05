# Azure AI Service Implementation For Image Analysis

This code is an implementation of multiple Azure AI services.
Make a request to post an image, and the code will run several steps below:

1. Upload the image to Azure Blob Storage
2. Run the image through Azure Computer Vision to get the image description
3. Translate the image description to Indonesian using Azure Translator
4. Return the translated text

The whole app is deployed on Azure Instance App

## How to Run Locally

1. Clone the repository

   ```shell
   git clone https://github.com/zeerafle/image-analysis-container.git
   ```

2. Create a file named `.env` in the root directory of the project
3. Create a resource group on Azure Portal

4. [Create multi-service AI services on Azure Portal](https://learn.microsoft.com/en-us/azure/ai-services/multi-service-resource?tabs=windows&pivots=azportal).
   Go to **Keys and Endpoint**, copy the **Key**, **Endpoint**, and **Location/Region**. Insert the values into
   the `.env` file with the following label:

   ```
   COGINITVE_SERVICE_KEY=your_key
   COGNITIVE_SERVICE_ENDPOINT=your_endpoint
   COGNITIVE_SERVICE_REGION=your_region
   ```

5. [Create a storage account on Azure Portal](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal).
   Go to **Access keys**, copy the **Connection string**. Insert the value into the `.env` file with the following
   label:

   ```
   STORAGE_CONNECTION_STRING=your_connection_string
   ```

6. Run the following commands to build docker image and run the container

   ```shell
   docker build -t image-analysis-container .
   docker run -d -p 5000:50505 --env-file .env image-analysis-container
   ```

7. Test the app by sending a POST request to `http://localhost:5000/` with an image file

## How to Deploy on Azure

Run the following command to deploy the Docker image to Azure Container Apps.

```bash
az countainerapp up \
  --resource-group your_resource_group \
  --name your_container_app_name \
  --ingress external \
  --target-port 50505 \
  --source .
```

If somehow it fails (like it did for me), you can push the Docker Image to Azure Container Registry and then create
Azure Container Apps from the image.
Remember to enable ingress and set the target port to 50505.
