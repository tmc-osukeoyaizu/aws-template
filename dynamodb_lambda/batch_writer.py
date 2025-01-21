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



# import boto3
# import uuid

# def lambda_handler(event, context):
#     table_name = 'serverless_workshop_intro'
#     dynamodb = boto3.resource('dynamodb')
#     table = dynamodb.Table(table_name)

#     result = None
#     people = [
#             { 'userid' : 'marivera', 'name' : 'Martha Rivera'},
#             { 'userid' : 'nikkwolf', 'name' : 'Nikki Wolf'},
#             { 'userid' : 'pasantos', 'name' : 'Paulo Santos'},
#         ]

#     with table.batch_writer() as batch_writer:
#         for person in people:
#             item = {
#                 '_id'     : uuid.uuid4().hex,
#                 'Userid'  : person['userid'],
#                 'FullName': person['name']
#             }
#             print("> batch writing: {}".format(person['userid']) )
#             batch_writer.put_item(Item=item)
            
#         result = f"Success. Added {len(people)} people to {table_name}."

#     return {'message': result}