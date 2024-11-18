import json
import base64
import boto3

client = boto3.client('dynamodb')
table_name = 'lab2-table'

def lambda_handler(event, context):
    
    print((event[0]['data']))
    print(base64.b64decode(event[0]['data']))
    # ただの文字列なのでキーを指定することができない
    data = base64.b64decode(event[0]['data']).decode('utf-8')
    print(data)
    
    # jsonデータなのでキーを指定してvalueを取得できる
    json_data = json.loads(data)
    print(json_data)
    
    data_id = json_data['id']
    data_timestamp = json_data['timestamp']
    data_spot = json_data['spot']
    data_temperature = json_data['temperature']
   
    item = {
        'id': {'S': data_id},
        'timestamp': {'N': str(data_timestamp)},
        'spot':{'S': data_spot},
        'temperature': {'N': str(data_temperature)}
    }
    
    client.put_item(TableName=table_name,Item=item)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
