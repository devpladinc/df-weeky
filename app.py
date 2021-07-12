from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world!"
    
@app.route('/about')
def welcome():
  return "Welcome to my Flask site, ©2018"
   
if __name__ == '__main__':
  # app.run(host='0.0.0.0', port=8080)
  app.run(host='0.0.0.0', port=port)