# command to zip files addObjects.py and test.txt 
zip -r addObjects.zip addObjects.py test.txt
# aws cli command to query for iam role arn that contains LambdaDeploymentRole in the name
aws iam list-roles --query 'Roles[?contains(RoleName, `LambdaDeploymentRole`) == `true`].Arn' --output text
# aws cli command to upload a lambda function code.zip file with addObjects.lambda_handler and runtime 3.12
aws lambda create-function --function-name addObjects --zip-file fileb://addObjects.zip --handler addObjects.lambda_handler --runtime python3.12 --role <arn>


Lambda関数のタイムアウト時間を変更する
