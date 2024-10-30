import json
import boto3

region = 'ap-northeast-1'
client = boto3.client('comprehend', region_name=region)

text = 'Amazon Comprehend is a natural language processing (NLP) service that uses machine learning to find insights and relationships in text.'
language_code = 'en'

def detect_key_phrases():
    response = client.detect_key_phrases(Text=text, LanguageCode=language_code)
    return response

def main():
    response = detect_key_phrases()
    print(response)
    print(response['KeyPhrases'][0]['Text'])
if __name__ == "__main__":
    main()