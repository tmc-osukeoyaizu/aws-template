import json
import boto3
import pymysql
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "lab2-secret"
    region_name = "ap-northeast-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']

    return secret

    # Your code goes here.

def lambda_handler(event, context):
    secret = json.loads(get_secret());
    # print(secret)
    rds_host = secret['host']
    rds_username = secret['username']
    rds_password = secret['password']
    rds_dbname = secret['dbname']

    con = pymysql.connect(host=rds_host, user=rds_username, password=rds_password, database=rds_dbname)
    with con.cursor() as cur:
        cur.execute('select * from table1')
        data = cur.fetchall()

    return {
        'statusCode': 200,
        'body': data
    }
