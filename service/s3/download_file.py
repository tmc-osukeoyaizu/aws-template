import json
import boto3

client = boto3.client('s3')

backet = 'lab2-s3'
file_key = 'test/test.txt'
local_file_path = '/tmp/oyaizu.txt'

client.download_file(backet, file_key, local_file_path)


def lambda_handler(event, context):
    with open(local_file_path) as f:
        data = f.read()
        print(data)
    return {
        'statusCode': 200,
        'body': 'OK'
    }
