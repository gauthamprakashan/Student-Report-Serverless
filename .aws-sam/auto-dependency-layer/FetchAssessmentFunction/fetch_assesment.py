import boto3
import simplejson as json  #use simplejson to to convert Decimal type into JSON
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Student_details')

def lambda_handler(event, context):
    print(event)
    if 'queryStringParameters' not in event:
        raise ValueError("Missing query string parameters")

    params = event['queryStringParameters']
        
    # Validate 'ID' parameter
    student_id = event['queryStringParameters']['ID']
    if not ID:
        raise ValueError("Missing 'ID' parameter")
    #student_id = event['queryStringParameters']['ID']
    if not assessment_name:
        raise ValueError("Missing 'assessment' parameter")
    assessment_name = event['queryStringParameters']['assessment']
    
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
