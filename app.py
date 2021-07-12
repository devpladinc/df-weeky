from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world!"
    
@app.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True)
  query_result = req.get('queryResult')
  print(query_result)
   
if __name__ == '__main__':
  # app.run(host='0.0.0.0', port=8080)
  app.run(host='0.0.0.0', port=port)