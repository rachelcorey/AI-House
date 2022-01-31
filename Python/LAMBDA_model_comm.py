import os, time, boto3, json

modelNames = {
    "kramer": "EP-kramer",
    "niles": "EP-niles"
}


def listToDblQuotes(listy):
    newList = []

    for strings in listy:
        newList.append('\"' + strings + '\"')

    newList = str(newList).replace('\'\"', '\"')
    newList = newList.replace('\"\'', '\"')
    newList = newList.replace('\\', '')
    newString = str(newList)
    return newString


def newQuery(query, past_inputs, past_responses):
    return """{
          "inputs": {
            "past_user_inputs": """ + listToDblQuotes(past_inputs) + """,
            "generated_responses": """ + listToDblQuotes(past_responses) + """,
            "text": """ + "\"" + query + "\"" + """
            }
        }"""


def queryBot(q, past_inputs, past_responses, which_bot):
    qFormat = newQuery(q, past_inputs, past_responses)
    # sendToModel = input_fn(qFormat, "application/json")
    runtime = boto3.client('sagemaker-runtime', region_name='us-east-1')
    response = runtime.invoke_endpoint(EndpointName='EP-'+which_bot,
                                       ContentType='application/json',
                                       Body=qFormat
                                       )
    botTextReply = json.loads(response['Body'].read()).get('generated_text')

    return botTextReply


def lambda_handler(event, context):
    query = event["inputs"]["text"]
    past_inputs = event["inputs"]["past_user_inputs"]
    generated_responses = event["inputs"]["generated_responses"]
    which_bot = event["inputs"]["which_bot"]

    botResponse = queryBot(query, past_inputs, generated_responses, which_bot)

    return {
        'statusCode': 200,
        'botResponse': botResponse,
    }


