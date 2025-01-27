import json
import os
import pymysql
import redis

rds_host = os.environ['RDS_HOST']
rds_username = os.environ['RDS_USER']
rds_password = os.environ['RDS_PASSWORD']
rds_dbname = os.environ['RDS_DB']
redis_host = os.environ['REDIS_HOST']
redis_port = os.environ['REDIS_PORT']

# mysql接続情報
con = pymysql.connect(host=rds_host, user=rds_username, password=rds_password, database=rds_dbname)

# redis接続情報
cache = redis.Redis(host=redis_host, port=redis_port, db=0)

# redis接続情報(転送中の暗号化有効)
# cache = redis.Redis(host=redis_host, port=redis_port, ssl=True, ssl_cert_reqs="none")

sql = 'select * from table1'

ttl = 10

def lambda_handler(event, context):
    
    res = cache.get(sql)
    
    if res:
        print('Cache exists!')
        return json.loads(res)
    
    print('Cache not exists...')
    with con.cursor() as cur:
        cur.execute(sql)
        res = cur.fetchall()
    
    print('Cache setting')
    
    # r.set(key, value_string ← json形式, ex=ttl)
    cache.set(sql, json.dumps(res), ex=ttl)
    return res
    
    
        
    return {
        'statusCode': 200,
        'body': res
    }

