import boto3
import time

client = boto3.client("sqs", region_name='ap-northeast-1')

queue_url = "https://sqs.ap-northeast-1.amazonaws.com/608728620263/lab2-queue.fifo"

response = client.send_message(
    QueueUrl=queue_url,
    MessageBody='Message 1',
    MessageDeduplicationId=str(time.time_ns()),    #MessageDeduplicationId=str(time.time_ns())でも可
    MessageGroupId='Group1'
)