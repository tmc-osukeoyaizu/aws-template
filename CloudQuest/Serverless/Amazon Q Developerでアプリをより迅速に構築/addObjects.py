import boto3
def lambda_handler(event, context):
    client = boto3.client('s3')
    response = client.list_buckets()
    for bucket in response['Buckets']:
        if bucket['Name'] == 'lab-s3-2':
            print('Bucket lab-s3-2 exists')
            return True
        else:
            #create the bucket
            client.create_bucket(Bucket='lab-s3-2')
            # upload test.txt to the S3 bucket
            client.upload_file('test.txt', 'lab-s3-2', 'test.txt')
            # create a new object in the bucket
            client.put_object(Bucket='lab-s3-2', Key='test2.txt', Body='test2.txt')
            # Enable versioning on the bucket
        client.put_bucket_versioning(Bucket='lab-s3-2', VersioningConfiguration={'Status': 'Enabled'})