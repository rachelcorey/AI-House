import boto3
from datetime import datetime
from datetime import timedelta

def lambda_handler(event, context):
    
    idle_threshold_hr = 1               # Change this to your threshold in hours
    
    cw = boto3.client('cloudwatch')
    sm = boto3.client('sagemaker')
    sns = boto3.client('sns')
    
    try:
        inservice_endpoints = sm.list_endpoints(
            SortBy='CreationTime',
            SortOrder='Ascending',
            MaxResults=100,
            # NameContains='string',     # for example 'dev-'
            StatusEquals='InService'
        )
        
        idle_endpoints = []
        for ep in inservice_endpoints['Endpoints']:
            
            ep_describe = sm.describe_endpoint(
                    EndpointName=ep['EndpointName']
                )
    
            metric_response = cw.get_metric_statistics(
                Namespace='AWS/SageMaker',
                MetricName='Invocations',
                Dimensions=[
                    {
                        'Name': 'EndpointName',
                        'Value': ep['EndpointName']
                        },
                        {
                         'Name': 'VariantName',
                        'Value': ep_describe['ProductionVariants'][0]['VariantName']                  
                        } 
                ],
                StartTime=datetime.utcnow()-timedelta(hours=idle_threshold_hr),
                EndTime=datetime.utcnow(),
                Period=int(idle_threshold_hr*60*60), 
                Statistics=['Sum'],
                Unit='None'
                )
    
            if int(metric_response['Datapoints'][0].get('Sum'))==0:     
                idle_endpoints.append(ep['EndpointName'])
        
        endpoint_result = ''
        if len(idle_endpoints) > 0:
            endpoint_result = 'idle endpoints found and deleted'
            print(idle_endpoints)
            replyList = []
            for endpoint in idle_endpoints:
                response = sm.delete_endpoint(EndpointName=endpoint)
                # reply = json.loads(response.text).get("Status")
                # replyList.append(reply)
            # response_sns = sns.publish(
            #     TopicArn='arn:aws:sns:us-east-1:816697443006:sns-idle-endpoint:a68ccf46-c0ee-4847-827f-40dd06eef1af',
            #     Message=str(replyList) + " The following endpoints have been idle for over {} hrs. Log on to Amazon SageMaker console to take actions.\n\n{}".format(idle_threshold_hr, '\n'.join(idle_endpoints)),
            #     Subject='Automated Notification: Idle Endpoints Detected',
            #     MessageStructure='string'
            # )
        else:
            endpoint_result = 'no idle endpoints were found...'
            
    
        return {'Status': str(endpoint_result)}
    
    except:
        return {'Status': 'Fail'}
