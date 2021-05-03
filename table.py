# Proj5
# Isabel Silva
# # aws access key id = prj5
# # access key = 1234
# # us-west-2
# # table
#
import boto3
from botocore.exceptions import ClientError
from botocore.errorfactory import *
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

# helper tool to delete current tables when testing
tbls = dynamodb.tables.all()
for i in tbls:
    #print(i)
    #i.delete()
    pass

# creates table in dynamodb, if table exists then it does nothing
def create_DM_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    try:
        table = dynamodb.Table('directMessages')
        #print(table)
        table.table_status
    except ClientError as e:
        error_code = e.response['Error']['Code']
        #print(error_code)
        if error_code == "ResourceNotFoundException":
            table = dynamodb.create_table(
                TableName = 'directMessages',
                KeySchema=[
                    {
                        'AttributeName':'mesgID',
                        'KeyType':'HASH'
                    },
                    {
                        'AttributeName':'timestamp',
                        'KeyType' : 'RANGE'
                    }

                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'mesgID',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'timestamp',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            table.meta.client.get_waiter('table_exists').wait(TableName='directMessages')
        else:
            print('ERROR')

