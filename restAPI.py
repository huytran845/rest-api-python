#An example frame of a RESTful Flask API

from flask import Flask, url_for, request, json, Response, jsonify
from functools import wraps
import logging

app = Flask(__name__)
file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

@app.route('/')
def api_root():
	return "Hello World\n"

@app.route('/articles')
def api_articles():
	return 'list of ' + url_for('api_articles') + '\n'

@app.route('/articles/<articleid>') #Can utilize path converters to change data type of articleid if needed with <type:articleid>, default is string.
def api_article(articleid):
	return 'You are reading ' + articleid + '\n'

@app.route('/hello_user') #Example if browser url is /hello_user, returns Jane Doe. If browser url has /hello_user?name=variable, it will return the variable instead.
def api_hello_user():
	if 'name' in request.args:
		return 'Hello ' + request.args['name'] + '\n'
	else:
		return 'Hello Jane Doe\n'

@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']) #Example of addressing requests based on the type requested.
def api_echo():
	if request.method == 'GET':
		return "ECHO: GET\n"
	elif request.method == 'POST':
		return "ECHO: POST\n"
	elif request.method == 'PATCH':
		return "ECHO: PATCH\n"
	elif request.method == 'PUT':
		return "ECHO: PUT\n"
	elif request.method == 'DELETE':
		return "ECHO: DELETE\n"

@app.route('/messages', methods = ['POST']) #Example for requesting data through a post. Displaying the data based on the content type.
def api_message():
	if request.headers['Content-Type'] == 'text/plain':
		return "Text Message: " + request.data + "\n"
	elif request.headers['Content-Type'] == 'application/json':
		return "JSON Message: " + json.dumps(request.json) + "\n"
	elif request.headers['Content-Type'] == 'application/octet-stream':
		f = open('./binary', 'wb')
		f.write(request.data)
		f.close()
		return "Binary message written!\n"
	else:
		return "Error 415 Unsupported Media Type\n"

@app.route('/hello', methods = ['GET']) #Example of a GET request where data being requested is returned in a JSON format through the API.
def api_hello():
    data = {
        'hello'  : 'world',
        'number' : 3
    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http:/youtube.com'

    return resp

@app.errorhandler(404) #Example of error handling in the API, when something is not found, the flask.jsonify is utilized to create a flask.Response() with the included content header. So we don't need the above Response() manual call.
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/users/<userid>', methods = ['GET']) #This function demonstrates the use of the error handling function, not_found() by having an example sample of data and checking the user values among them.
def api_users(userid):
    users = {'1':'john', '2':'steve', '3':'bill'}
    
    if userid in users:
        return jsonify({userid:users[userid]})
    else:
        return not_found()

def check_auth(username, password): #check_auth is a function that verifies if the username and password are correct. Currently, it is a skeleton function that only allows the username admin and password secret.
	return username == 'admin' and password == 'secret'

def authenticate(): #The authenticate function returns a message to the user to authenticate in the situation where authentification fails.
	message = {'message': "Authenticate.\n"}
	resp = jsonify(message)

	resp.status_code = 401
	resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

	return resp

def requires_auth(f): #Tested with curl -v -u "admin:secret" http://127.0.0.1:5000/secrets which is the authenticated user. This is a decorator that takes the function f.
	@wraps(f) #This is from the functool library copies the decorator function so that doctools can properly recognize the function without function information being lost. I.E. requires_auth will show instead of decorated.
	def decorated(*args, **kwargs):
		auth = request.authorization #If authorization is empty then it becomes None
		if not auth: 
			return authenticate()

		elif not check_auth(auth.username, auth.password): #Checks if the inputed information is correct, if not then output same message
			return authenticate()
		return f(*args, **kwargs) #Returns with a function call to the original function if successful since layers of authentication have been successfully passed.

	return decorated

@app.route('/secrets')
@requires_auth
def api_secrets():
	return "Successfully accessed hidden information!\n"

@app.route('/logging', methods = ['GET'])
def api_logging():
    app.logger.info('informing')
    app.logger.warning('warning')
    app.logger.error('This is an example error message!')
    
    return "Check your logs\n"

if __name__ == '__main__':
	app.run(host='0.0.0.0') #use app.run(debug=True) to run debug mode