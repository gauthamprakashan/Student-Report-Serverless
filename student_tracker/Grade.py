

MAX_MARKS = 600
def lambda_handler(event, context):
    Grade = []
    data =  event['Payload']['Input'][0]
    percentage = event['Payload']['Input'][1]
    for i in range(len(percentage)):
        grade = []
        #Calculates grade and stores it in a list of lists
        for j in range(len(percentage[0])):
            if percentage[i][j] >= 70:
                grade.append('A') 
            elif percentage[i][j] >= 50:
                grade.append('B') 
            elif percentage[i][j] >= 35:
                grade.append('C') 
            else:
                grade.append('D')
        Grade.append(grade)
    return {
        "statusCode": 200,
        "body": "Percentage Collected",
        'output3': [data, percentage, Grade]
     
    }
     