import boto3
from decimal import Decimal
dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table('Student_details')

def lambda_handler(event, context):
    # implement run for looop each ith value for 3 arrays
    data = event['Payload']['Input'][0]
    assessments = ["Finalexam","Assement1","Assement2","Assement5","Assement6","Midterm","Assement3","Assement4"]
    subjects = ["maths", "science", "social", "kannada", "english", "hindi"]
    # Define the percentage value you want to add
    your_percentage_value_list = event['Payload']['Input'][1]  # Example percentage value
    
    grade_value_list = event['Payload']['Input'][2]
    
    # Perform the put_item operation to update the item
    #can't use put have to use update
    
    for i in range(len(data)):
        key_value = data[i]['ID']
        
        your_percentage=your_percentage_value_list[i]
        
        item = data[i]
        for j in range(len(assessments)):
            your_percentage_value=Decimal(str(your_percentage_value_list[i][j]))
            grade_value=grade_value_list[i][j]
            print(assessments[j],your_percentage_value,grade_value,key_value)
            assessment = assessments[j]

            print(item[assessment][subjects[0]])
            
            update_expression = f"set #a.#m = :m, #a.#sci = :sci, #a.#so = :so, #a.#e = :e, #a.#h = :h, #a.#k = :k"
            response = table.update_item(
                Key={"ID": key_value},
                UpdateExpression=update_expression,
                ExpressionAttributeNames={"#a": assessment,"#m": "maths","#sci": "science", "#so": "social", "#e": "english", "#h":"hindi", "#k" : "kannada" },
                ExpressionAttributeValues={":m": item[assessment][subjects[0]], ":sci": item[assessment][subjects[1]], ":so": item[assessment][subjects[2]], ":e": item[assessment][subjects[3]], ":h": item[assessment][subjects[4]], ":k":item[assessment][subjects[5]] }
                )
                
            update_expression = f"set #a.#p = :p, #a.#g = :g"
            
            response = table.update_item(
                Key={"ID": key_value},
                UpdateExpression=update_expression,
                ExpressionAttributeNames={"#a": assessment,"#p": "percentage","#g": "grade"},
                ExpressionAttributeValues={":p": your_percentage_value, ":g":grade_value  }
                )
            print(response)
    return { #if else condition
        "statusCode": 200,
        "body": "Data Stored",
     
    }
        
