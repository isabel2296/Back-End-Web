# Proj5
# Isabel Silva

import table as t
from table import *
import logging.config

import textwrap
import bottle
from bottle import * #import get, post, request, response, template, redirect
from boto3.dynamodb.conditions import Key, Attr
import requests
import uuid
#set up app and logging
app = bottle.default_app()
app.config.load_config('./etc/app.ini')

logging.config.fileConfig(app.config['logging.config'])

# client url
CT_URL = 'http://localhost:5100/'

# create table
t.create_DM_table(t.dynamodb)

# retrieve table from dynamdb
try:
    table = t.dynamodb.Table('directMessages')
except ClientError as e:
    if e.response['Error']['Code'] == "ResourceNotFoundException":
        print("Table: 'directMessages' does not exist")

# counter for msgID since dynamoDB does not generate unique identifiers


if not sys.warnoptions:
    import warnings
    warnings.simplefilter('ignore', ResourceWarning)
'''Helper functions: 
get_name_from_id access the client microservice to get username based on ID
'''
def get_name_from_id(id):
    urlRequest = CT_URL + id + '/name'  # url to get name from client server
    rr = requests.get(urlRequest)  # gets the values using kv.py command...
    return rr.json()['name'][0]['userName']

def get_ID_from_name(name):
    urlRequest = CT_URL + name + '/ID'  # url to get name from client server
    rr = requests.get(urlRequest)  # gets the values using kv.py command...
    print(rr.json()['ID'][0]['userID'])
    return rr.json()['ID'][0]['userID']

# home screen ; displays a "proj5 hello" message
# http localhost:5000/
@get('/')
def home():
    return textwrap.dedent('''
        <h1> Proj5 Hello</h1>\n''')

# http POST localhost:5000/user/sendDM senderID=1 receiverID=3 message='hello' quickReplies='None'
@post('/user/sendDM')
def sendDirectMessage():
    data = request.json #get user information
    timestamp = datetime.now() # get message current time
    msgID = uuid.uuid4() # this will be the unique id for mesgID key in dynamaboDB
    if not data:
        abort(400,"no data entereed")

    posted_fields = data.keys()
    required_fields = {'senderID', 'receiverID', 'message', 'quickReplies'}
    # make sure we get the necessary information from user
    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    usrName = get_name_from_id(data['senderID']) # get user name from client server

    try:
    # add the dm message with timestamp to local dynamoDB DM table
        table.put_item(
            Item={
                'mesgID': str(msgID),
                'timestamp': str(timestamp),
                'username': usrName,
                'senderID': str(data['senderID']),
                'reciverID': str(data['receiverID']),
                'message': str(data['message']),
                'quickReply': str(data['quickReplies'])
            }
        )
    except ClientError as e:
        abort(409, str(e.response['Error']['Code'])) # if unable to add to DM error will display

    response.status = 200
    response.set_header('Location', f"/user/sendDM/{data}")
    #get dm to send it as a json string back
    resp = table.get_item(Key={
        'mesgID': str(msgID),
        'timestamp': str(timestamp)}
        )
    return {"DM":resp['Item']}

# http POST localhost:5000/user/sendDM mesgID='2c57b962-f536-4120-9f87-223723d18fad' message='hello' senderID=5
@post('/user/replyDM')
def replyToDM():
    data = request.json
    timestamp = datetime.now()  # message current time
    #msgID = uuid.uuid4()  # unique id mesgID key in dynamaboDB
    if not data:
        abort(400, "no data entereed")

    posted_fields = data.keys()
    required_fields = {'mesgID', 'message', 'senderID'}

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    output = table.query(KeyConditionExpression=Key('mesgID').eq(data['mesgID']), ScanIndexForward=False, Limit=1)
    sendID = output['Items'][0]['reciverID']
    recID = output['Items'][0]['senderID']
    if sendID != str(data['senderID']):
        temp = sendID
        sendID = recID
        recID = temp
    try:
        msg = str(data['message'])
        if output['Items'][0]['quickReply'] != 'None':
            if msg == "0":
                msg = "Yes"
            elif msg == "1":
                msg = "No"
            elif msg == "3":
                msg = "Call me"
        table.put_item(
            Item={
                'username': get_name_from_id(output['Items'][0]['reciverID']),
                'mesgID': data['mesgID'],
                'timestamp': str(timestamp),
                'senderID': sendID,
                'reciverID': recID,
                'message': msg,
                'quickReply': 'None'
            }
        )
    except ClientError as e:
        abort(400,'Unable to reply')
    response.status = 200
    response.set_header('Location', f"/user/replyDM/{data}")
    resp = table.get_item(Key={
        'mesgID': data['mesgID'],
        'timestamp': str(timestamp)}
    )
    return {"Reply":resp['Item']}

# http localhost:5000/bob%20smith/dms
# list the dms that the user has recieved
# gets all DMS at the recieverID matches with the userName
@get('/<userName>/dms')
def listDirectMessageFor(userName):
    resp = table.scan(
        FilterExpression=Attr('reciverID').eq(str(get_ID_from_name(userName)))
    )
    response.status = 200
    response.set_header('Location', f"/user/dms")
    title = userName + "'s DM's"
    return {title: resp['Items']}

# http localhost:5000/2c57b962-f536-4120-9f87-223723d18fad/replies
@get('/<mesgID>/replies')
def listDmReplies(mesgID):
    resp = table.query(
        KeyConditionExpression=Key('mesgID').eq(mesgID),
        ScanIndexForward=False
    )
    response.status = 200
    response.set_header('Location', f"/mesgID/replies")
    return {"Replies": resp['Items']}

# helper calls to view all entries in the DM table
''' http localhost:5000/allMesg'''
@get('/allMesg')
def getAllEntries():
    entries = table.scan()
    response.status = 200
    response.set_header('Location', f"/allDMs")
    return {'All_Entries':entries['Items']}
