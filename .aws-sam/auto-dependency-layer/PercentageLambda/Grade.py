

MAX_MARKS = 600
def lambda_handler(event, context):
    grade = []
    data =  event['Payload']['Input'][0]
    percentage = event['Payload']['Input'][1]
    for i in range(len(percentage)):
        if percentage[i] >= 70:
            grade.append('A') 
        elif percentage[i] >= 50:
            grade.append('A') 
        elif percentage[i] >= 35:
            grade.append('A') 
        else:
            grade.append('A')
    return {
        "statusCode": 200,
        "body": "Percentage Collected",
        'output3': [data, percentage, grade]
     
    }
     