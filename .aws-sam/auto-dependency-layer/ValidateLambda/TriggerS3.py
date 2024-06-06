import os
import json
import boto3

s3_client = boto3.client('s3')
my_state_machine_arn = os.environ['STATE_MACHINE_ARN']
client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    print(event)
    for record in event['Records']:
        response = client.start_execution(
            stateMachineArn=my_state_machine_arn,
            input=json.dumps(record['s3'])
        )