import json

def lambda_handler(event, context):
    token = event['headers']['authorizationToken']
    method_arn = event['methodArn']
    
    if validate_token(token):
        return generate_policy('user', 'Allow', method_arn)
    else:
        return generate_policy('user', 'Deny', method_arn)

def validate_token(token):
    valid_tokens = ['abc-123', 'xyz-456']  # Example valid tokens
    if token in valid_tokens:
        return True
    else:
        return False

def generate_policy(principal_id, effect, resource):   #generates policy to allow or deny
    auth_response = {}
    auth_response['principalId'] = principal_id
    if effect and resource:
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': resource
                }
            ]
        }
        auth_response['policyDocument'] = policy_document
    return auth_response
