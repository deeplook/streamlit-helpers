import boto3
import requests


def translate_text(
    text,
    source_lang=None,
    target_lang=None,
    aws_access_key_id="",
    aws_secret_access_key="",
):
    """Translate text using AWS Translate cloud service.
    
    See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html
    """
    client = boto3.client(
        "translate",
        region_name="us-east-1",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    resp = client.translate_text(
        Text=text,
        TerminologyNames=[
            # 'string',
        ],
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang,
        Settings={
            # 'Profanity': 'MASK'
        }
    )
    return resp
