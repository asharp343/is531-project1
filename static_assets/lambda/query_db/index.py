import json
import boto3
import os

def lambda_handler(event, context):
    
    rds = boto3.client('rds-data')
    
    
    response = rds.execute_statement(
        resourceArn = os.environ['CLUSTER_ARN'],
        secretArn = os.environ['SECRET_ARN'],
        sql = 'SELECT * FROM donuts'
    )
    
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(response['records'])
    }