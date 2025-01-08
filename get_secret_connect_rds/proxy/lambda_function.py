import json
import boto3
import psycopg2
from botocore.exceptions import ClientError

region = 'ap-northeast-1'

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
    proxy_host = secret['proxy_host']
    rds_host = secret['host']
    rds_port = secret['port']
    rds_username = secret['username']
    rds_password = secret['password']
    rds_dbname = secret['dbname']
    
    client = boto3.client('rds',region_name=region)
    token = client.generate_db_auth_token(DBHostname=proxy_host, Port=rds_port, DBUsername=rds_username, Region=region)
    
    con = psycopg2.connect(host=proxy_host, user=rds_username, password=token, dbname=rds_dbname, sslrootcert='AmazonRootCA1.pem', sslmode='verify-ca')

    with con.cursor() as cur:
        cur.execute('select * from table1')
        data = cur.fetchall()
        print(data)

    return {
        'statusCode': 200,
        'body': data
    }