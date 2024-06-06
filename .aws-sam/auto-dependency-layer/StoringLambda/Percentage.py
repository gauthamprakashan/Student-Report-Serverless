import boto3


s3_client = boto3.client('s3')

dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table('Student_details')

MAX_MARKS = 600
def lambda_handler(event, context):
    List_Percentage= []
    #print(event['Payload']['Input'])
    data = event['Payload']['Input']
    
    #print(data[0])
    assessments = ["Finalexam","Assement1","Assement2","Assement5","Assement6","Midterm","Assement3","Assement4"]
    list1 = []
    for i in range(len(data)):
        #Access each record
        item = data[i]
        #print(item['Assessments'])
        List_Percentage = []
        for key,values in item.items():
            total_count =0
            #Calculate percentage from given set of assessment keys
            if key in assessments: 
                print(values)
                dict = values
                for score in dict.values():
                    score = int(score)
                    

                    if score == "":
                         return {
                            "statusCode": 400,
                            "body": "Emplty Marks Field",
                        }
                        
                    total_count +=score
                percentage = total_count/MAX_MARKS * 100
                List_Percentage.append(percentage)
        list1.append(List_Percentage)
    print(List_Percentage)
    #Percentage's are stored in a list of list for each assesment within each record
    return {
        "statusCode": 200,
        "body": "Percentage Collected",
        'output2': [data, list1]
     
    }
    
