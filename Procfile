mesgapp: python3 -m bottle --bind localhost:$PORT --debug --reload msgapp
clientAPI: python3 -m bottle --bind=localhost:$PORT --debug --reload api
timeLineAPI: python3 -m bottle --bind=localhost:$PORT --debug --reload timelinesAPI
dynamoDb: java -Djava.library.path=./dynamodb_local_latest/DynamoDBLocal_lib -jar ./dynamodb_local_latest/DynamoDBLocal.jar -sharedDb

