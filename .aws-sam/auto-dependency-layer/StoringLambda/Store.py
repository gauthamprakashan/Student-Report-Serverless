import boto3
from decimal import Decimal
dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table('Student_details')

def lambda_handler(event, context):
    
    #Initalsing array's from input
    data = event['Payload']['Input'][0]
    assessments = ["Finalexam","Assement1","Assement2","Assement5","Assement6","Midterm","Assement3","Assement4"]
    subjects = ["maths", "science", "social", "kannada", "english", "hindi"]

    your_percentage_value_list = event['Payload']['Input'][1]  
    
    grade_value_list = event['Payload']['Input'][2]
    
    
    
    for i in range(len(data)):
        key_value = data[i]['ID']
        
        
        #access  each record
        item = data[i]
        for j in range(len(assessments)):
            your_percentage_value=Decimal(str(your_percentage_value_list[i][j]))
            grade_value=grade_value_list[i][j]
            #print(assessments[j],your_percentage_value,grade_value,key_value)
            assessment = assessments[j]

            #print(item[assessment][subjects[0]])
            
            #Update each record with the marks of each assesment
            update_expression = f"set #a.#m = :m, #a.#sci = :sci, #a.#so = :so, #a.#e = :e, #a.#h = :h, #a.#k = :k"
            response = table.update_item(
                Key={"ID": key_value},
                UpdateExpression=update_expression,
                ExpressionAttributeNames={"#a": assessment,"#m": "maths","#sci": "science", "#so": "social", "#e": "english", "#h":"hindi", "#k" : "kannada" },
                ExpressionAttributeValues={":m": item[assessment][subjects[0]], ":sci": item[assessment][subjects[1]], ":so": item[assessment][subjects[2]], ":e": item[assessment][subjects[3]], ":h": item[assessment][subjects[4]], ":k":item[assessment][subjects[5]] }
                )
            

            #update each record with the percentage and grade we calculated
            update_expression = f"set #a.#p = :p, #a.#g = :g"
            
            response = table.update_item(
                Key={"ID": key_value},
                UpdateExpression=update_expression,
                ExpressionAttributeNames={"#a": assessment,"#p": "percentage","#g": "grade"},
                ExpressionAttributeValues={":p": your_percentage_value, ":g":grade_value  }
                )
            print(response)

    return { 
        "statusCode": 200,
        "body": "Data Stored",
     
    }
        
