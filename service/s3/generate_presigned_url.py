import os
import boto3
import json

# Lambdaの環境変数からフォルダ名とバケット名を取得
folder_name = 'test'
bucket_name = 'lab2-s3'

def lambda_handler(event, context):
    # API Gatewayからのクエリストリングパラメータ取得
    # file_name = event['queryStringParameters']['fileName']
    file_name = 'test.txt'

    # 署名付きURLの有効期限（秒）
    expiration_time = 60 * 60  # 1時間

    # AWS SDKの設定
    s3 = boto3.client('s3')

    # フォルダ名とファイル名を組み合わせてオブジェクトキーを生成
    object_key = f'{folder_name}/{file_name}'

    try:
        # 署名付きURLの生成
        signed_url = s3.generate_presigned_url(
            ClientMethod = 'get_object',
            Params = {'Bucket' : bucket_name, 'Key' : object_key},
            ExpiresIn = expiration_time,
            HttpMethod = 'GET'
            )
        return {
            'statusCode': 200,
            'body': json.dumps({'signedUrl': signed_url})
        }
    except Exception as e:
        print('Error generating signed URL:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }




# 確認方法
# curl -X PUT --upload-file <ローカルのファイル> '<署名付きURL>' 