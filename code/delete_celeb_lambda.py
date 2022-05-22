import boto3
from boto3.dynamodb.conditions import Key
import os

def handler(event, context):

    # event properties
    name = event['queryStringParameters']['celebName']
    
    # environment and ssm variables    
    FUNCTION_REGION = os.environ['awsRegion']

    ssmClient = boto3.client('ssm', region_name=FUNCTION_REGION)
    dynamoDB_tablename = ssmClient.get_parameter(Name='/params/dynamoDbTable')['Parameter']['Value']
    
    # DynamoDB properties
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamoDB_tablename)

    # deleting records connected with the celeb
    response = table.scan()
    data = response['Items']

    number_of_deleted = 0
    for doc in data:
        if name in doc['FoundCelebs']:
            try:
                table.delete_item(
                    Key={'RequestId': doc['RequestId']}
                )
                number_of_deleted += 1
            except Exception as e:
                print("Unable to delete data from DynamoDB table, error: {}".format(e))

    return {
        'statusCode': 200,
        'body': f"deleted {number_of_deleted} elements"
    }
