import boto3
import os
import json
from decimal import Decimal

table_name = os.environ['TABLE_NAME']
dynamodb = boto3.client('dynamodb', region_name='ap-northeast-1')

def decimal_to_int(obj):
    if isinstance(obj, Decimal):
        return int(obj)

def lambda_handler(event, context):
    httpMethod = event['httpMethod']
    
    
    if httpMethod == 'GET':
        #DynamoDBデータ取得
        scan_data = dynamodb.scan(TableName=table_name)
        return {
            'statusCode': 200,
            'body': json.dumps(scan_data['Items'], default=decimal_to_int)
        }
    else:
        id_data = event['queryStringParameters']['id']
        text_data = event['queryStringParameters']['text']
        item = {            
                'id' : {"N" : str(id_data)},
                'text' : {"S" : text_data}
            }
        print(item)
        
        #DynamoDBデータ挿入
        dynamodb.put_item(TableName=table_name,Item=item)
        return {
            'statusCode': 200,
            'body': 'insert success'
        }  
