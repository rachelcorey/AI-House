import boto3, requests, json, time
from sagemaker_inference import content_types, encoder, decoder


model_names = ['kramer', 'niles']

def input_fn(input_data, content_type):
  return decoder.decode(input_data, content_type)


def format_req(model_name):
  return """{
  "model": \""""  + model_name +   """\"
}"""

###### call lambda for creating endpoints ######
def create_ep(ep_name):
  AWS_API_CALL = AWS_HOST + "/beta/createEP"
  sendToFunc = input_fn(format_req(ep_name), "application/json")
  response = requests.post(AWS_API_CALL, json=sendToFunc.tolist())
  createReply = json.loads(response.text)
  print (createReply)
  return


##### call lambda for checking endpoints' status ######
def get_endpoint_status():
  AWS_API_CALL = AWS_HOST + "/beta/statusEP"
  response = requests.post(AWS_API_CALL)
  reply = json.loads(response.text).get("response")
  return reply


def init_endpoints():
  statusReply = get_endpoint_status()
  for model_name in model_names:
    if statusReply[model_name] == 'none':
      print(model_name + " endpoint not found. creating endpoint.....")
      create_ep(model_name)
  print("All endpoints are created. Verifying status...")
  check_status()
  return


def check_status():
  statuses = []
  all_ep_ready = False

  while not all_ep_ready:
    statusReply = get_endpoint_status()
    for model_name in model_names:
      endpoint_status = statusReply.get(model_name)
      print(model_name + ": " + endpoint_status)
      statuses.append(endpoint_status)
    if 'Creating' not in statuses:
      all_ep_ready = True
      print("All endpoints are ready to go!")
    else:
      statuses.clear()
      print("Endpoints not ready yet. Checking again in 30s....")
      time.sleep(30)
  
  return

if __name__ == '__main__':

  init_endpoints()





