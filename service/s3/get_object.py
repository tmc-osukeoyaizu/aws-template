import json
import boto3

client = boto3.client('s3')

# バケット名,オブジェクト名
BUCKET_NAME = 'lab2-sns-s3'

def lambda_handler(event, context):
    print(event)
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    bucket = sns_message['Records'][0]['s3']['bucket']['name']
    key = sns_message['Records'][0]['s3']['object']['key']
    print(bucket, key)
    response = client.get_object(Bucket=bucket, Key=key)
    body = response['Body'].read()
    decoded_body = body.decode()
    # print(response)
    print(type(body), type(decoded_body))
    print(decoded_body)
    return {
        'statusCode': 200,
        'body': 'OK'
    } 