import boto3
import simplejson as json  #use simplejson to to convert DynamoDB's Decimal type into JSON

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Students')

def lambda_handler(event, context):
    if event.get('queryStringParameters') is None:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'No Parameter'})
        }
        # Validate 'ID' parameter
    params = event['queryStringParameters']
    if 'ID' in event['queryStringParameters']:
        student_id = event['queryStringParameters']['ID']
    else:
        return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No ID Parameter'})
            }
    assessments = ["Finalexam","Assement1","Assement2","Assement5","Assement6","Midterm","Assement3","Assement4"]

    try:
        response = table.get_item(Key={'ID': student_id})
        print(response)
        if 'Item' in response:
            item = response['Item']
            assessments = {k: v for k, v in item.items() if k in assessments }
            if any(isinstance(v, dict) and not v for v in assessments.values()):
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'All assessments not there'})
                }
            
            return {
                'statusCode': 200,
                'body':  json.dumps(assessments)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Student not found'})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
