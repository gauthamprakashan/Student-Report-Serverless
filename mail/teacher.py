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
table = dynamodb.Table('Students')

def lambda_handler(event, context):
    try:
        # Constants
        if event.get('queryStringParameters') is None:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No Parameter'})
            }

        params = event['queryStringParameters']
        # Validate 'class' parameter
        class1 = params.get('Class', None) if isinstance(params.get('Class', None), str) else None
        if class1 is None:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No class Parameter'})
            }

        #teachers_email = event['queryStringParameters']['teachers_email']
        FROM_EMAIL = 'gautham.prakashan@antstack.io'
        subject = 'Assessment Details'
        
        # Retrieve the object data from DynamoDB
        
        
        expr = Key('Class').eq(class1)
        response = table.scan(FilterExpression=expr)
        assessments = ["Finalexam","Assement1","Assement2","Assement5","Assement6","Midterm","Assement3","Assement4"]
        log = []
        if 'Items' in response and 'Items'!= []:
            items = response['Items']
            
            
            print(items)
            
            for item in items:
                flattened_data = []
                flat_data1= []
                info_row = {
                    'ID': item['ID'],
                    'Name': item.get('Name', ''),
                    'Class': item.get('Class', ''),
                    'DOB': item.get('DOB', '')
                }
                
                csv_file = StringIO()
                csv_writer = csv.writer(csv_file)
                print(item.get('parents_contact_email_1', ''))
                csv_writer.writerow(["Yearly report"]) 
                print(item['parents_contact_email_1'])
                parent_contact = item.get('parents_contact_email_1', '') or item.get('parents_contact_email_2', '')
                if not parent_contact:
                    log.append(f"Missing parent contact email for student ID: {item['ID']}")
                    continue  # Skip this student if no parent contact email
                print(parent_contact)
                flat_data1.append(info_row)
                print(item)
                assessments = {k: v for k, v in item.items() if k in assessments }
                for assessment_name, scores in assessments.items():
                    row = {'Assessment': assessment_name}
                    row.update(scores)
                    flattened_data.append(row)
                    print(flattened_data)
            # # Create a CSV file in memory
                
            # print(flat_data1)
            # #print(flat_data1[0].keys())
            # print(type(flat_data1[0]))
                csv_writer = csv.DictWriter(csv_file, fieldnames = flat_data1[0].keys())
            
                csv_writer.writeheader()
                csv_writer.writerows(flat_data1)
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([' '])
                csv_writer.writerows([' '])
                
                csv_writer.writerow([" ", "subjects"])
                csv_writer = csv.DictWriter(csv_file, fieldnames=flattened_data[0].keys())
                csv_writer.writeheader()
                csv_writer.writerows(flattened_data)
                
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([' '])
                csv_writer.writerows([' '])
            # Get the CSV file content
                csv_file_content = csv_file.getvalue()

            # Create the MIME container for the email
                msg = MIMEMultipart()
                msg['Subject'] = subject
                msg['From'] = FROM_EMAIL
                msg['To'] = parent_contact
                
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
                    Destinations=[parent_contact],
                    RawMessage={'Data': msg.as_string()}
                )

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Emails sent successfully!', 'LOG': log})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Students not found', 'LOG' : log})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error sending email: {str(e)}')
        }

