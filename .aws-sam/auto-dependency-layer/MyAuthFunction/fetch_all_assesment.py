import boto3
import simplejson as json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Student_details')

def lambda_handler(event, context):
    student_id = event['queryStringParameters']['ID']
    assessments = ["Finalexam","Assement1","Assement2","Assement5","Assement6","mid-term","Assement3","Assement4"]

    try:
        response = table.get_item(Key={'ID': student_id})
        print(response)
        if 'Item' in response:
            item = response['Item']
            assessments = {k: v for k, v in item.items() if k in assessments }
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
