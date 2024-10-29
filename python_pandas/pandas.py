import json
import boto3
import pandas as pd

client = boto3.client('s3')

backet = 'lab2-lambda'
file_key = 'data.csv'
local_file_path = '/tmp/data.csv'

client.download_file(backet, file_key, local_file_path)


def lambda_handler(event, context):
    df = pd.read_csv('/tmp/data.csv')

    df['amount'] = df['price'] * df['pieces']
    
    # print(df)
    
    ans = {}
    ans['sum'] = int(df['amount'].sum())
    ans['max'] = int(df['amount'].max())
    ans['min'] = int(df['amount'].min())
    ans['mean'] = int(df['amount'].mean())
    ans['median'] = int(df['amount'].median())


    return {
        'statusCode': 200,
        'body': json.dumps(ans)
    }
