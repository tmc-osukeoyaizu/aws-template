import json
import boto3
import os

client = boto3.client('dynamodb')
table_name = os.environ['TABLE']

def lambda_handler(event, context):
    data = client.scan(TableName=table_name)
    
    return {
        'statusCode': 200,
        'body': data
    }
