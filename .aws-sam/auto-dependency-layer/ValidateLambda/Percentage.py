import json
import boto3
import csv


s3_client = boto3.client('s3')

dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table('Student_details')

MAX_MARKS = 600
def lambda_handler(event, context):
    List_Percentage= []
    #print(event['Payload']['Input'])
    data = event['Payload']['Input']
    assessments = ["Finalexam","Assement1","Assement2","Assement5","Assement6","mid-term","Assement3","Assement4"]
    print(data)
    
    for i in range(len(data)):
        

        item = data[i]
        print(item)
        for key,values in item.items():
            total_count =0
            print(key)
            if key in assessments: #extend
                print(values)
                dict = values
                for score in dict.values():
                    
                    total_count +=score
                percentage = total_count/MAX_MARKS * 100
                List_Percentage.append(percentage)
    print(List_Percentage)
    
    return {
        "statusCode": 200,
        "body": "Percentage Collected",
        'output2': [data, List_Percentage]
     
    }