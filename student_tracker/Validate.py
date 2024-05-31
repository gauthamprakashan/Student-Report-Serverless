import boto3
import csv

s3_client = boto3.client('s3')

#Reformats CSV data from excel into Dictonary 
def reformat_record(record, assessments):
    reformatted = {
        'ID': record['ID'],
        'Name': record['Name'],
        'class': record['class'],
        'DOB': record['DOB'],
    }

    for assessment in assessments:
        subjects = {key.split('-')[1]: value for key, value in record.items() if key.startswith(assessment)}
        if subjects:
            reformatted[assessment] = subjects

    return reformatted

def lambda_handler(event, context):
    # Print the event for debugging purposes
    #print(event)
    
    # Access the required keys from the input event
    key = event['Payload']['Input']['object']['key']
    bucket_name = event['Payload']['Input']["bucket"]["name"]
    
    # Retrieve the object data from S3
    s3_response = s3_client.get_object(Bucket=bucket_name, Key=key)

    # Extract the object's data (file content)
    file_data = s3_response["Body"].read().decode('utf-8')
    csv_data = csv.DictReader(file_data.splitlines())
    
    # List of dictionaries to store the CSV data
    item_list = []

    assessments = ["Finalexam","Assement1","Assement2","Assement5","Assement6","Midterm","Assement3","Assement4"]

    for assessment_record in csv_data:
        # Access data based on field names
        student_id = assessment_record.get('ID')
        student_name = assessment_record.get('Name')
        student_class = assessment_record.get('class')
        if not student_id:
            print("Error: Student ID is missing in the assessment record.")
            continue  # Skip further validation if student ID is missing
        
        if not isinstance(student_name, str) or not student_name.strip():
            print(f"Error: Student name is missing or not a string for ID {student_id}.")
            continue  # Skip further validation if student name is missing or not a string
        
        
        if not student_class:
            print(f"Error: Class is missing for ID {student_id}.")
            continue
        
        valid_assessment = True
        for assessment in assessments:
        # Check if assessment fields are present and not empty
            for subject in ['maths', 'science', 'social', 'kannada', 'english', 'hindi']:
                field_value = assessment_record.get(f"{assessment}-{subject}")
                if not field_value:
                    print(f"Error: One or more fields are missing for {assessment} for ID {student_id}.")
                    valid_assessment = False
                    break
                elif not field_value.isdigit():  # Check if the value is not empty and is a digit
                    print(f"Error: {assessment}-{subject} for ID {student_id} is not a valid integer.")
                    valid_assessment = False
                    break
            else:
                continue  # Proceed to the next assessment if all fields are present and valid

            break 
        
        if not valid_assessment:
            continue
        
       
        
        # Reformat the record to nest assessments
        reformatted_record = reformat_record(assessment_record, assessments)
        
        # Append the entire valid reformatted record to the item_list
        item_list.append(reformatted_record)
    print(item_list)
    if not item_list:
        return {
            'statusCode': 400,  
            'body': "No valid data found"  
        }
    
    
    return {
        'statusCode': 200,
        'body': "Data collected and validated",
        'output1': item_list
    }
