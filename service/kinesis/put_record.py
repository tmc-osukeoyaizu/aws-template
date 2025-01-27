import boto3
import json
import random
import string
import datetime

STREAM_NAME = "lab2-stream"
client = boto3.client("kinesis",region_name='ap-northeast-1')


def make_data(i):
    data = {}
    now = datetime.datetime.now()
    data["id"] = "device%s" % (i)
    data["timestamp"] = int(now.timestamp() * 1000)
    data["spot"] = random.choice(list(string.ascii_uppercase))
    data["temperature"] = random.randint(10, 40)
    return data


if __name__ == "__main__":
    for i in range(0,100):
        data = json.dumps(make_data(i))
        p_key = str(random.randint(1, 100))
        # Kinesisへレコード送信
        client.put_record(
            StreamName=STREAM_NAME,
            Data=data,
            PartitionKey=p_key
        )