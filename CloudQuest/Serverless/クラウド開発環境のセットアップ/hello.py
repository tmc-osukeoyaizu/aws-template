client = boto3.client('s3')
	
def upload_file(file_name, bucket, object_name):
    client.upload_file(file_name, bucket, object_name)