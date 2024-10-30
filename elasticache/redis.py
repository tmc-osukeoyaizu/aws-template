import json
import redis
import pymysql
import os

redis_host = os.environ['REDISHOST']
rds_host = os.environ['RDSHOST']
rds_user = os.environ['USER']
rds_password = os.environ['PASSWORD']
rds_db = os.environ['DB']

# ElastiCache Redisクライアントの設定
redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0)

# RDS MySQLクライアントの設定
con = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, database=rds_db)
# Cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, ssl=True, ssl_cert_reqs="none")


sqlstr = 'select * from table1'

def get_user_info(sql):
    
    # キャッシュからデータを取得
    cached_data = redis_client.get(sql)
    if cached_data:
        print('redis', cached_data)
        return cached_data
    
    # キャッシュにデータがない場合、RDSから取得
    with con.cursor() as cur:
        cur.execute(sql)
        result = cur.fetchall()
        print('rds', result)
    
    # データをキャッシュに保存
    redis_client.set(sql, json.dumps(result), ex=10)
    return result

def lambda_handler(event, context):
    
    response = get_user_info(sqlstr)
    print('response', response)
    return {
        'statusCode': 200,
        'body': response
    }
