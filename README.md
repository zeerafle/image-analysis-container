# Azure AI Service Implementation For Image Analysis

This code is an implementation of multiple Azure AI services.
Make a request to post an image, and the code will run several steps below:

1. Upload the image to Azure Blob Storage
2. Run the image through Azure Computer Vision to get the image description
3. Translate the image description to Indonesian using Azure Translator
4. Return the translated text

The whole app is deployed on Azure Instance App