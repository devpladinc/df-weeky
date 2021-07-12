from flask import Flask, request
from helpers.intent_handlers import Integrator


app = Flask(__name__)

@app.route('/')
def server_healthcheck():
    return "Hello world!"
    
@app.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True)
  query_result = req.get('queryResult')
  df_action = query_result.get('action')

  Integrator.check_intent(df_action)

  print(query_result)
  return {
        "fulfillmentText": 'This is from the heroku webhook',
        "source": 'webhook'
    }
   
if __name__ == '__main__':
  # app.run(host='0.0.0.0', port=8080)
  app.run(host='0.0.0.0', port=port)