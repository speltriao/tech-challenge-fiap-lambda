import json
import pg8000
import os

def lambda_handler(event, context):
    token = event['headers'].get('teste')
    method_arn = event['methodArn']
    
    print(f"Authorization Token: {token}")
    print(f"Method ARN: {method_arn}")
    
    if token == "SIM":
        if is_able_to_connect_to_database():
          return generate_policy('user', 'Allow', method_arn)
        return generate_policy('user', 'Deny', method_arn)
    elif token == "NAO":
        return generate_policy('user', 'Deny', method_arn)
    else:
        raise Exception('Unauthorized!!!!!!!!!!!!')

def generate_policy(principal_id, effect, resource):
    auth_response = {}
    auth_response['principalId'] = principal_id
    
    if effect and resource:
        policy_document = {}
        policy_document['Version'] = '2012-10-17'
        policy_document['Statement'] = []
        
        statement = {}
        statement['Action'] = 'execute-api:Invoke'
        statement['Effect'] = effect
        statement['Resource'] = resource
        
        policy_document['Statement'].append(statement)
        auth_response['policyDocument'] = policy_document
    
    return auth_response
  

def is_able_to_connect_to_database():
    db_host = os.environ['DB_HOST']
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    try:
        connection = pg8000.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        print(connection)
        cursor = connection.cursor()
        print(cursor)
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        print(f"Database version: {result[0]}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
      return False
