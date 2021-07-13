from flask import Flask, request
from helpers import intent_handlers as handler


app = Flask(__name__)

@app.route('/')
def server_healthcheck():
    return "Hello world!"
    
@app.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True)
  query_response = req.get('queryResult')
  try:
    action = query_response.get('action')
    spiel =  handler.check_intent(action)
    return spiel
  
  except Exception as e:
    intent_name = query_response.get('intent')  
    params = query_response.get('parameters')
    action = intent_name.get('displayName')

  print("query: ", query_response)
  print("intent: ", intent_name)
  print("action: ",action)
  print('params:', params)

  if action == 'check.topic':
    params = params.get('topic')
  if action == 'check.topc.ds':
    params = params.get('t-datascience')  

  spiel =  handler.check_intent(action, params)
  return spiel
   
if __name__ == '__main__':
  # app.run(host='0.0.0.0', port=8080)
  app.run(host='0.0.0.0', port=port)