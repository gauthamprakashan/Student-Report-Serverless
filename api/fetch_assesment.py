import boto3
import simplejson as json  #use simplejson to to convert Decimal type into JSON
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Students')

def lambda_handler(event, context):
    print(event)
    if event.get('queryStringParameters') is None:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'No Parameter'})
        }
    
    
    # Validate 'ID'and 'assesment' parameter
    if 'ID' in event['queryStringParameters']:
        student_id = event['queryStringParameters']['ID']
    else:
        return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No ID Parameter'})
            }
   
    if 'assessment' in event['queryStringParameters']:
        assessment_name = event['queryStringParameters']['assessment']
    else:
        return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No assement Parameter'})
            }
    
    try:
        response = table.get_item(Key={'ID': student_id})
        if 'Item' in response:
            assessment_details = response['Item'].get(assessment_name, "Assessment not found")
            return {
                'statusCode': 200,
                'body': json.dumps({assessment_name: assessment_details})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Student not found'})
            }
    
    except Exception as e:
        print("sus")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
