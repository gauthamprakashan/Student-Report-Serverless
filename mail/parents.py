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
table = dynamodb.Table('Student_details')
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    try:
        #constants
        ID = event['queryStringParameters']['ID']
        parents_email = event['queryStringParameters']['parents_email']
        FROM_EMAIL = 'gautham.prakashan@antstack.io'
        subject = 'Assessment Details'
        
        # Retrieve the object data from DynamoDB
        expr = boto3.dynamodb.conditions.Key('ID').eq(ID)
        assessments = ["Finalexam","Assement1","Assement2","Assement5","Assement6","Midterm","Assement3","Assement4"]
        response = table.scan(FilterExpression=expr)
        print(response)
       
        if 'Items' in response:
            
            item = response['Items'][0]
            print(type(item))
            #retrive parents_email with get_item
            assessments = {k: v for k, v in item.items() if k in assessments }

            flattened_data = []
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
    
            # Upload the CSV file to S3
            #s3_client.put_object(Body=csv_file_content, Bucket=bucket_name, Key=csv_file_key)
            

            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = FROM_EMAIL
            msg['To'] = parents_email

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
                Destinations=[event['queryStringParameters']['parents_email']],
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
    
        
        # Send email to teachers
        

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error sending email: {str(e)}')
        }
