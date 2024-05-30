import json
import boto3
import csv
from io import StringIO
from decimal import Decimal
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from boto3.dynamodb.conditions import Key

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
ses_client = boto3.client('ses')
table = dynamodb.Table('Student_details')

def lambda_handler(event, context):
    try:
        # Constants
        class1 = event['queryStringParameters']['class']
        teachers_email = event['queryStringParameters']['teachers_email']
        FROM_EMAIL = 'gautham.prakashan@antstack.io'
        subject = 'Assessment Details'
        
        # Retrieve the object data from DynamoDB
        expr = Key('class').eq(class1)
        response = table.scan(FilterExpression=expr)
        assessments = ["Finalexam","Assement1","Assement2","Assement5","Assement6","mid-term","Assement3","Assement4"]
        print(response)
        if 'Items' in response:
            items = response['Items']
            flattened_data = []
            

            for item in items:
                print(item)
               
                assessments = {k: v for k, v in item.items() if k in assessments }
                for assessment_name, scores in assessments.items():
                    row = {'ID': item['ID'], 'Assessment': assessment_name}
                    row.update(scores)
                    flattened_data.append(row)

            # Create a CSV file in memory
            csv_file = StringIO()
            csv_writer = csv.DictWriter(csv_file, fieldnames=flattened_data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(flattened_data)
            
            # Get the CSV file content
            csv_file_content = csv_file.getvalue()

            # Create the MIME container for the email
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = FROM_EMAIL
            msg['To'] = teachers_email

            # Email body
            body = MIMEText('Please find the Classes Report Card details in the CSV file.', 'plain')
            msg.attach(body)

            # Attach the CSV file
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(csv_file_content)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename='report.csv')
            msg.attach(part)

            # Send the email
            ses_response = ses_client.send_raw_email(
                Source=FROM_EMAIL,
                Destinations=[teachers_email],
                RawMessage={'Data': msg.as_string()}
            )

            return {
                'statusCode': 200,
                'body': json.dumps('Email sent successfully!')
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Students not found'})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error sending email: {str(e)}')
        }

