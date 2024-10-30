import json
import boto3

region = 'ap-northeast-1'
client = boto3.client('comprehend', region_name=region)

text = 'Amazon Comprehend is a natural language processing (NLP) service that uses machine learning to find insights and relationships in text.'

def detect_dominant_language():
    response = client.detect_dominant_language(Text=text)
    return response

def main():
    response = detect_dominant_language()
    print(response['Languages'][0]['LanguageCode'])

if __name__ == "__main__":
    main()