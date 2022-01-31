import os, time, boto3, json, ast, requests
from sagemaker_inference import content_types, encoder, decoder
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

AWS_API_CALL = AWS_HOST + "/beta/sendtext"

# Decode a JSON response from the server
def input_fn(input_data, content_type):
  return decoder.decode(input_data, content_type)

# Turns the list of strings into double quotes instead of single, for JSON property formatting
def listToDblQuotes(listy):
  newList = []

  for strings in listy:
      newList.append('\"' + strings + '\"')

  newList = str(newList).replace('\'\"', '\"')
  newList = newList.replace('\"\'', '\"')
  newList = newList.replace('\\', '')
  newString = str(newList)
  return newString

# Format a JSON query
def newQuery(query, past_inputs, past_responses, which_bot):
  return """{
      "inputs": {
          "past_user_inputs": """ + listToDblQuotes(past_inputs) + """,
          "generated_responses": """ + listToDblQuotes(past_responses) + """,
          "text": """ + "\"" + query + "\"" + """,
          "which_bot": """ + "\"" + which_bot + "\"" + """
      }
  }"""

# Query an endpoint
def queryBot(q, past_inputs, past_responses, which_bot):
  sendToModel = newQuery(q, past_inputs, past_responses, which_bot)
  sendToModel = input_fn(sendToModel, "application/json")
  botTextReply = None
  counter = -1

  while botTextReply is None:
    response = requests.post(AWS_API_CALL, json=sendToModel.tolist())
    botTextReply = json.loads(response.text).get("botResponse")
    counter += 1
    if counter > 0:
      print("Endpoint timed out " + str(counter) + " times... retrying...")

  # Append the past inputs and responses to the ongoing list, so the bots can have a context for their reply
  past_inputs.append(q)
  past_responses.append(botTextReply)

  return botTextReply

# Cull the past responses and inputs so we don't overload the model
def cullArr(past):
  if len(past) == 3:
    past = []
  return past

if __name__ == '__main__':
  past_inputs1 = []
  responses1 = []
  past_inputs2 = []
  responses2 = []

  query1 = "Hey, how's Jerry?"
  print("***First bot initialized with: " + query1)

  while 1:
    query2 = queryBot(query1, past_inputs1, responses1, "kramer")

    print("Kramer says:  " + str(query2))

    time.sleep(0.1)

    query1 = queryBot(query2, past_inputs2, responses2, "niles")

    print("Niles says:  " + str(query1))

    past_inputs1 = cullArr(past_inputs1)
    past_inputs2 = cullArr(past_inputs2)
    responses1 = cullArr(responses1)
    responses2 = cullArr(responses2)

