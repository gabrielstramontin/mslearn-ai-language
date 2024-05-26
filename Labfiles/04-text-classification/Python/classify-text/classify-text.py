# First, install the Azure AI Language Text Analytics SDK package: [pip install azure-ai-textanalytics==5.3.0]

from dotenv import load_dotenv
import os

# Import Namespaces:
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        # Get Configuration Settings:
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')
        project_name = os.getenv('PROJECT')
        deployment_name = os.getenv('DEPLOYMENT')

        # Create client using Endpoint and Key:
        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

        # Read each text file in the articles folder:
        batchedDocuments = []
        articles_folder = 'articles'
        files = os.listdir(articles_folder)
        for file_name in files:
            
            # Read the File Contents:
            text = open(os.path.join(articles_folder, file_name), encoding='utf8').read()
            batchedDocuments.append(text)

        # Get Classifications:
        operation = ai_client.begin_single_label_classify(batchedDocuments, project_name=project_name, deployment_name=deployment_name)
        document_results = operation.result()
        for doc, classification_result in zip(files, document_results):
            if classification_result.kind == "CustomDocumentClassification":
                classification = classification_result.classifications[0]
                print("{} was classified as '{}' with confidence score {}.".format(doc, classification.category, classification.confidence_score))
            elif classification_result.is_error is True:
                print("{} has an error with code '{}' and message '{}'".format(doc, classification_result.error.code, classification_result.error.message))

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()

# At the end, in the integrated terminal, enter the following command to test and run the program: [python classify-text.py]
