# UserId-Point-index (GSI)
#   パーティションキー:UserId
#   ソートキー:Point

# GameId-index (LSI)
#   パーティションキー:GameId


import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('lab2-dynamodb')

def get_userId_point():
  response = table.query(
    IndexName='UserId-Point-index',
    KeyConditionExpression=Key('UserId').eq('U001') & Key('Point').gt(50)
  )
  return response['Items']


def get_gameId():
  response = table.query(
    IndexName='GameId-index',
    KeyConditionExpression=Key('GameId').eq('G001')
  )
  return response['Items']

def lambda_handler(event, context):
    print(get_userId_point())
    print(get_gameId())
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

#インデックス設定なしの場合
# import boto3
# from boto3.dynamodb.conditions import Key, Attr

# def lambda_handler(event, context):
    
#     dynamoDB = boto3.resource("dynamodb")
#     table = dynamoDB.Table("lab2-dynamodb") 

#     # UserIdがU001、Pointが50以上の全レコードを取得
#     queryData1 = table.query(
#       KeyConditionExpression = Key("UserId").eq("U001"),
#       FilterExpression = Attr("Point").gt(50)
#     )
    
#     print(queryData1['Items'])
    
#     # UserIdがU002、GameIdがG001、Pointが50以上の全レコードを取得
#     queryData2 = table.query(
#       KeyConditionExpression = Key("UserId").eq("U002") & Key("GameId").eq("G001"),
#       FilterExpression = Attr("Point").gt(50)
#     )
    
#     print(queryData2['Items'])
    
#     # GameIdがG001の全レコード取得
#     queryData3 = table.scan(
#     FilterExpression=Attr('GameId').eq('G001')
# )
    
#     print(queryData3['Items'])
  
#     return 200
