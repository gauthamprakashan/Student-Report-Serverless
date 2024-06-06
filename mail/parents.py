import json
import boto3
import csv
from io import StringIO

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')
ses_client = boto3.client('ses')
table = dynamodb.Table('Students')
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    try:
        #constants

        if event.get('queryStringParameters') is None:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No Parameter'})
            }

        #params = event['queryStringParameters']
        
        # Validate 'ID' parameter
        if 'ID' in event['queryStringParameters']:
            ID = event['queryStringParameters']['ID']
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No ID Parameter'})
            }
        
        
        
        FROM_EMAIL = 'gautham.prakashan@antstack.io'
        subject = 'Assessment Details'
        
        # Retrieve the object data from DynamoDB
        expr = boto3.dynamodb.conditions.Key('ID').eq(ID)
        assessments = ["Finalexam","Assement1","Assement2","Assement5","Assement6","Midterm","Assement3","Assement4"]
        response = table.scan(FilterExpression=expr)
        print(response)
       
        if 'Items' in response:
            
            item = response['Items'][0]
            print(item)
            #print(item['parents_contact_email_1'])
            print("no")
            
            parents_email = item['parents_contact_email_1'] or item['parents_contact_email_2'] 
            
            
            if parents_email == "":
                return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No Email in DB'})
            }
            
            print(type(parents_email))

            assessments = {k: v for k, v in item.items() if k in assessments and isinstance(v, dict) and v}

            flattened_data = []

            #Access data and flatten it from retrieved response from DynamoDB
            for assessment_name, scores in assessments.items():
                row = {'Assessment': assessment_name}
                row.update(scores)
                flattened_data.append(row)
            # Create a CSV file in memory
            csv_file = StringIO()
            csv_writer = csv.DictWriter(csv_file, fieldnames=flattened_data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(flattened_data)
            
            csv_file_content = csv_file.getvalue()
    
            
            
#           #Creating raw email in SES to send attachments
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = FROM_EMAIL
            msg['To'] = item['parents_contact_email_1'] or item['parents_contact_email_2']

            # Email body
            body = MIMEText('Please find childs Report Card details in the CSV file.', 'plain')
            msg.attach(body)

            # Attach the CSV file
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(csv_file_content)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename='report.csv')
            msg.attach(part)

            response = ses_client.send_raw_email(
                Source=FROM_EMAIL,
                Destinations=[parents_email],
                RawMessage={
                    'Data': msg.as_string()
                }
            )

            return {
                'statusCode': 200,
                'body': json.dumps('Email sent successfully!')
            }
            
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Student not found'})
            }
    
        
        

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error sending email: {str(e)}')
        }
