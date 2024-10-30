import json
import boto3

region = 'ap-northeast-1'
client = boto3.client('comprehend', region_name=region)

text = 'Amazon Comprehend is a natural language processing (NLP) service that uses machine learning to find insights and relationships in text.'
language_code = 'en'

def detect_entities():
    response = client.detect_entities(Text=text, LanguageCode=language_code)
    return response

def main():
    response = detect_entities()
    print(response['Entities'][0]['Text'], response['Entities'][0]['Type'])
    print(response['Entities'][1]['Text'], response['Entities'][1]['Type'])

if __name__ == "__main__":
    main()