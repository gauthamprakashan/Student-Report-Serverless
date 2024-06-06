import json
import boto3
import logging
import os
from botocore.exceptions import ClientError

def create_presigned_url(bucket_name, object_name,expiration=3600):
    """Generate a presigned URL to upload an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    content_type = 'text/csv'
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name,
                                                            'ContentType': content_type},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return response

def lambda_handler(event, context):
    # Parse the request body
    
    query_parameters = event.get('queryStringParameters')
    if query_parameters is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Query parameters are missing'})
        }
    
    file_name = query_parameters.get('file_name')
    if file_name is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'file_name parameter is missing'})
        }
    
    if not file_name:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'File name is required'})
        }

    # Generate the presigned URL
    bucket_name = os.environ['BUCKET_NAME']
    print(bucket_name)
    #bucket_name = 'presign-demo1'
    presigned_url = create_presigned_url(bucket_name, file_name)
    
    if presigned_url is None:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Could not generate presigned URL'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'presigned_url': presigned_url})
    }
