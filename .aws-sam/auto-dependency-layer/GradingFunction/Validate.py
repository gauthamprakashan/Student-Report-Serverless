import json
import boto3
import csv

s3_client = boto3.client('s3')
dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table('Student_details')

def lambda_handler(event, context):
    # Print the event for debugging purposes
    #print(event['input'])
    #data = json.loads(event)
    print(event)
    # Access the required keys from the input event
    key = event['Payload']['Input']['object']['key']
    bucket_name = event['Payload']['Input']["bucket"]["name"]
    
    # Retrieve the object data from S3
    s3_response = s3_client.get_object(Bucket=bucket_name, Key=key)

    # Extract the object's data (file content)
    file_data = s3_response["Body"].read().decode('utf-8')
    csv_data = csv.DictReader(file_data.splitlines())
    
    # List of dictionaries
    item_list = []

    # Iterate over each row in the CSV data
    for assessment_record in csv_data:
        # Access data based on field names
        student_id = assessment_record.get('ID')
        student_name = assessment_record.get('Name')
        #parent_email = assessment_record.get('parents_contact_email_1')
        if not student_id:
            print("Error: Student ID is missing in the assessment record.")
            continue  # Skip further validation if student ID is missing
        
        if not isinstance(student_name, str) or not student_name.strip():
            print(f"Error: Student name is missing or not a string for ID {student_id}.")
            continue  # Skip further validation if student name is missing or not a string
        
        # if not parent_email:
        #     print(f"Error: Parent's email is missing for student {student_name} (ID: {student_id}).")
        #     continue  # Skip further validation if parent's email is missing
        
        
        response = table.get_item(Key={'ID': student_id})
        if 'Item' in response:
            print("Item found for ID", student_id)
            item_list.append(response['Item'])
        else:
            print("No item found for ID", student_id)

    # Add more validation checks if needed
    return {
        'statusCode': 200,
        'body': "Data collected and validated",
        'output1': item_list
    }
