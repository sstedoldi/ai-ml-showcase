import boto3 
from awssecrets import aws_secrets

bedrock = boto3.client(service_name='bedrock',
                       region_name=aws_secrets["REGION"],
                       aws_access_key_id=aws_secrets["AWS_KEY"],
                       aws_secret_access_key=aws_secrets["AWS_SECRET"])

llms_info = bedrock.list_foundation_models()

print(llms_info)