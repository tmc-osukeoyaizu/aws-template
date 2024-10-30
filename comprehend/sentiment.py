import json
import boto3

region = 'ap-northeast-1'
client = boto3.client('comprehend', region_name=region)

text = 'hello'
language_code = 'en'

def detect_sentiment():
    response = client.detect_sentiment(Text=text, LanguageCode=language_code)
    return response

def main():
    response = detect_sentiment()
    print(response['Sentiment'])

if __name__ == "__main__":
    main()