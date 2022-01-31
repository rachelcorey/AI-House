import json, boto3

def lambda_handler(event, context):
    client = boto3.client('sagemaker')
    
    model_statuses = {
        'kramer' : 'none',
        'niles' : 'none',
        'fake' : 'none',
        'placeholder' : 'none',
        'notyet' : 'none',
        'testing' : 'none'
    }

    # print the status of the endpoint
    endpoint_list = client.list_endpoints()["Endpoints"]
    for endpoint in endpoint_list:
        endpoint_name = endpoint['EndpointName'][3:]
        print("endpoint name: " + endpoint_name)
        endpoint_status = endpoint['EndpointStatus']
        print("endpoint status: " + endpoint_status)
        model_statuses[endpoint_name] = endpoint_status

    return {
        'statusCode': 200,
        'response' : model_statuses,
        'body': json.dumps('Successfully retreived statuses.')
    }

