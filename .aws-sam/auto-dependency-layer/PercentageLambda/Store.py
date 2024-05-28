import boto3
from decimal import Decimal
dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table('Student_details')

def lambda_handler(event, context):
    # implement run for looop each ith value for 3 arrays
    data = event['Payload']['Input'][0]
    assessments = ["Finalexam","Assement1","Assement2","Assement5","Assement6","mid-term","Assement3","Assement4"]
    # Define the percentage value you want to add
    your_percentage_value_list = event['Payload']['Input'][1]  # Example percentage value
    
    grade_value_list = event['Payload']['Input'][2]
    
    print(data,your_percentage_value_list,grade_value_list)
    # Perform the put_item operation to update the item
    #can't use put have to use update
    
    for i in range(len(data)):
        key_value = data[i]['ID']
        your_percentage_value=Decimal(str(your_percentage_value_list[i]))
        grade_value=grade_value_list[i]
        for assessment in assessments:
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
        
