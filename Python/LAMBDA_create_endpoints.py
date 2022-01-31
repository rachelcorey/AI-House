import boto3, json

def lambda_handler(event, context):
    client = boto3.client('sagemaker')
    
    endpoint_pfx = 'EP-'
    endpoint_config_pfx = 'EC-'
    
    model_name = event["model"]
    
    ####### Create ########
    create_endpoint_response = client.create_endpoint(
      EndpointName=endpoint_pfx + model_name,
      EndpointConfigName=endpoint_config_pfx + model_name)
    print(create_endpoint_response['EndpointArn'])
    print('EndpointArn = {}'.format(create_endpoint_response['EndpointArn']))
  
    # get the status of the endpoint
    response = client.describe_endpoint(EndpointName=endpoint_pfx + model_name)
    status = response['EndpointStatus']
    print('EndpointStatus = {}'.format(status))
    #################

    return {'Status': status}
