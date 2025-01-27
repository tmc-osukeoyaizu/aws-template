import json
import boto3
import datetime

USERS_TABLE = 'lab2-table'
dynamodb = boto3.resource('dynamodb')
ddbTable = dynamodb.Table(USERS_TABLE)

response_body = {'Message': 'Unsupported route'}
status_code = 400
headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
    }

def lambda_handler(event, context):
    print(event)
    httpMethod = event['httpMethod']
    queryStringParameters = event['queryStringParameters']
    body = event['body']

    print(httpMethod)
    print(queryStringParameters)
    print(body)
    

    # クエリパスで分岐させる場合はroute_key変数を使用する
    # pathParameters = event['pathParameters']
    # print(pathParameters)
    # route_key = f"{event['httpMethod']} {event['resource']}"
    # print(route_key)
    

    try:
        # テーブルからデータを取得する
        if httpMethod == 'GET':
            # クリアパラメータで指定されているidデータを取得する
            if queryStringParameters:
                ddb_response = ddbTable.get_item(
                    Key={'id': queryStringParameters['id']}
                )
                response_body = ddb_response['Item']
            # クエリパラメータの指定がない場合は全件取得する
            else:
                response = ddbTable.scan()
                response_body = response['Items']
            status_code = 200

        # クエリパラメータで指定されているidデータを削除する
        if httpMethod == 'DELETE':
            ddbTable.delete_item(
                Key={
                    'id': queryStringParameters['id']
                    }
            )
            response_body = f'DELETE id:{queryStringParameters['id']} Succsess!!'
            status_code = 200

        # リクエストボディのデータを登録する
        if httpMethod == 'POST':
            item = json.loads(body)
            item['timestamp'] = datetime.datetime.now().isoformat()
            ddbTable.put_item(Item=item)
            response_body = f'POST {item} Succsess!!'
            status_code = 200
        
        # リクエストボディのデータのname列をクエリパラメータで指定したnameの値に変更する
        if httpMethod == 'PUT':
            # update item in the database
            item = json.loads(body)
            item['name'] = queryStringParameters['name']
            item['timestamp'] = datetime.datetime.now().isoformat()
            # update the database
            ddbTable.put_item(
                Item=item
            )
            response_body = f'PUT {item} Succsess!!'
            status_code = 200

    except Exception as err:
        status_code = 400
        response_body = {'Error:': str(err)}
        print(str(err))

    return {
        'statusCode': 200,
        'body': json.dumps(response_body)
    }
