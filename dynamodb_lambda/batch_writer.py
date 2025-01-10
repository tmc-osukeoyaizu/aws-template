import json
import boto3

dynamo = boto3.resource('dynamodb')
dynamo_table = dynamo.Table('lab2-table')

def lambda_handler(event, context):
    items = [
                {
                    "UserId": "U001",
                    "GameId": "G001",
                    "Game": "レース",
                    "Point": 80
                },
                {
                    "UserId": "U001",
                    "GameId": "G002",
                    "Game": "シューティング",
                    "Point": 40
                },    
                {
                    "UserId": "U002",
                    "GameId": "G001",
                    "Game": "レース",
                    "Point": 70
                },
                {
                    "UserId": "U002",
                    "GameId": "G002",
                    "Game": "シューティング",
                    "Point": 85
                }

            ]
    with dynamo_table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
