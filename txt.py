from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient

endpoint = "https://cloud-input.cognitiveservices.azure.com/"
credential = AzureKeyCredential("81bd20d2555e4bc2b603e3819361b99e")
source_container_sas_url_en = "https://doinp.blob.core.windows.net/dostranslaterinp?sp=rl&st=2023-07-11T04:41:32Z&se=2023-07-11T12:41:32Z&spr=https&sv=2022-11-02&sr=c&sig=k70BV8%2FUSBRmWbRyvKCGmtpjJa%2FkUSPOjcZb4j9kLj0%3D"
target_container_sas_url_es = "https://doinp.blob.core.windows.net/translateddocs?sp=rcwl&st=2023-07-11T04:42:36Z&se=2023-07-11T12:42:36Z&spr=https&sv=2022-11-02&sr=c&sig=zAFsotzgBfR1W8hl0oaIPGcxiYf8mIevuD5GIVHg%2BGo%3D"

document_translation_client = DocumentTranslationClient(endpoint, credential)

poller = document_translation_client.begin_translation(source_container_sas_url_en, target_container_sas_url_es, "es")

result = poller.result()

print(f"Status: {poller.status()}")
print(f"Created on: {poller.details.created_on}")
print(f"Last updated on: {poller.details.last_updated_on}")
print(f"Total number of translations on documents: {poller.details.documents_total_count}")

print("\nOf total documents...")
print(f"{poller.details.documents_failed_count} failed")
print(f"{poller.details.documents_succeeded_count} succeeded")

for document in result:
    print(f"Document ID: {document.id}")
    print(f"Document status: {document.status}")
    if document.status == "Succeeded":
        print(f"Source document location: {document.source_document_url}")
        print(f"Translated document location: {document.translated_document_url}")
        print(f"Translated to language: {document.translated_to}\n")
    else:
        print(f"Error Code: {document.error.code}, Message: {document.error.message}\n")