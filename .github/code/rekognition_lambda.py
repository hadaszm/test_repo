import json
import boto3
import base64
import io
import uuid
from datetime import datetime
import os
def handler(event, context):
    
    photo = json.loads(event['body'])["base64img"]
    
    # environment and ssm params
    FUNCTION_REGION = os.environ['awsRegion']
    
    # request params 
    request_id = str(uuid.uuid4())
    request_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    # recognize
    try:
        client=boto3.client('rekognition')
        imgdata = base64.b64decode(str(photo))
        response = client.recognize_celebrities(Image={'Bytes': io.BytesIO(imgdata).read()})
    except Exception as err:
        print(f"Error in recogniizing celebrities: {err}")
        raise
    
    # extract names
    celebs = []
    for celebrity in response['CelebrityFaces']:
        print(f"Found celebrity:  {celebrity['Name']}")
        celebs.append(celebrity['Name'])

    # invoke save results lambda 
    try:
        saveResultsLambdaClient = boto3.client('lambda', region_name=FUNCTION_REGION)
        dbParameters = {"request_id": request_id, "request_time": request_time, "celeb_names": celebs}
        response = saveResultsLambdaClient.invoke(FunctionName = 'SaveResultsLambda', InvocationType = 'RequestResponse', Payload = json.dumps(dbParameters))
        httpStatusCode = response["ResponseMetadata"]["HTTPStatusCode"]
    except Exception as err:
        print(f"Error in invoking save results lamnda: {err}")
        raise
    
    if not (httpStatusCode>=200 and httpStatusCode<300):
        print(f"Error in invoking save results lamnda. HttpStatusCode is {httpStatusCode}")
        raise
    
    # return results
    response_body = {"request_id": request_id, "request_time": request_time, "celeb_names": celebs}
    return {
        'statusCode': 200,
        'body': json.dumps(response_body)
    }