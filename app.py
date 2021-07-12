from flask import Flask, request
from helpers import intent_handlers as handler


app = Flask(__name__)

@app.route('/')
def server_healthcheck():
    return "Hello world!"
    
@app.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True)
  query_result = req.get('queryResult')
  action = query_result.get('action')

  handler.check_intent(action)

  print(query_result)
  return {
        "fulfillmentText": 'This is from the heroku webhook',
        "source": 'webhook'
    }
   
if __name__ == '__main__':
  # app.run(host='0.0.0.0', port=8080)
  app.run(host='0.0.0.0', port=port)