from flask import Flask, request, render_template
from redis import client
from helpers import intent_handlers as handler
from logs.utils import logging as log
import redis
import uuid

app = Flask(__name__)
redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)


@app.route('/')
def server_healthcheck():
    return render_template('df_messenger.html')
    
@app.route('/webhook', methods=['POST'])
def webhook():

  # init bot user
  # bot_user = str(uuid.uuid4())
  # bot_init = {"init" : "true", "webhook" : "success"}
  # redis_client.hmset(bot_user, bot_init)

  req = request.get_json(silent=True, force=True)
  query_response = req.get('queryResult')
  print("query response:", query_response)

  try:
    action = query_response.get('action')

    if action == 'checktopic.yes-getlist.checktopic':
      params = query_response.get('queryText')

    spiel =  handler.check_intent(action, params)
    return spiel
  
  except Exception as e:
    intent_name = query_response.get('intent')  
    params = query_response.get('parameters')
    
    action = intent_name.get('displayName')
    log.info('Action %s', action)
    
    if action == 'check.topic':
      params = params.get('topic')
    elif action == 'input.unknown':
      params = ""
    elif action == 'Default Welcome Intent':
      params = ""
    elif action == 'checktopic.yes-getlist':
      params = ""
    elif action == 'checktopic.no-askmenu':
      params = ""
    elif action == 'checktopic.no.yes.backmenu':
      params = ""
    elif action == 'checktopic.no.no-topicstay':
      params = ""
    elif action == 'check.see.more':
      params = ""
    elif action == 'check.ds-yes':
      params = ""
    elif action == 'check.ml-yes':
      params = ""
    elif action == 'check.pl-yes':
      params = ""
    elif action == 'check.ds-no':
      params = ""
    elif action == 'check.ml-no':
      params = ""
    elif action == 'check.pl-no':
      params = ""
    elif action == 'call.menu.handle':
      params = ""
    elif action == 'check.data.science':
      params = ["Data science"]
    elif action == 'check.machine.learning':
      params = ["Machine Learning"]
    elif action == 'check.programming':
      params = ["Programming language"]
    
  print("PARAMS SENT:", params)
  # print("BOT USER:", bot_user)
  # spiel =  handler.check_intent(bot_user, action, params)
  spiel =  handler.check_intent(action, params)

  return spiel
   
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
  # app.run(host='0.0.0.0', port=port)