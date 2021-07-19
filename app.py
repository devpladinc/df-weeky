from flask import Flask, request, render_template
from helpers import intent_handlers as handler
from logs.utils import logging as log
from helpers.api_handlers import Wiki_API as wiki

app = Flask(__name__)

@app.route('/')
def server_healthcheck():
    return render_template('df_messenger.html')

    
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
    log.info('Action %s', action)

    if action == 'check.topic':
      params = params.get('topic')
    # if action == 'check.topic.ds':
    #   params = params.get('t-datascience')
    if action == 'check.topic.programming':
      params = params.get('t-programming')
      print('PARAMS:', params)
      handler.send_summary(params)
      payload = {
        "fulfillmentText": "dummy",
        "source": 'webhook'
      }
      return payload

  spiel =  handler.check_intent(action, params)
  return spiel
   
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
  # app.run(host='0.0.0.0', port=port)