import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError

try:
    endpoint = os.environ["COGNITIVE_SERVICE_ENDPOINT"]
    key = os.environ["COGNITIVE_SERVICE_KEY"]
    region = os.environ["COGNITIVE_SERVICE_REGION"]
except KeyError:
    print("Missing environment variable 'COGNITIVE_SERVICE_ENDPOINT' or 'COGNITIVE_SERVICE_KEY' or 'COGNITIVE_SERVICE_REGION'.")
    exit()

text_translator = TextTranslationClient(endpoint=endpoint, credential=TranslatorCredential(key, region))


def translate_text(text: str):
    try:
        source_lang = 'en'
        target_lang = ['id']
        input_text_elements = [InputTextItem(text=text)]

        response = text_translator.translate(
            content=input_text_elements,
            to=target_lang,
            from_parameter=source_lang
        )
        translation = response[0] if response else None

        if translation:
            for translated_text in translation.translations:
                print("Translated text: ", translated_text.text)
                return translated_text.text

    except HttpResponseError as e:
        if e.error is not None:
            print("Error code: ", e.error.code)
            print("Message: ", e.error.message)
        raise

