#An example frame of a RESTful Flask API

from flask import Flask, url_for, request, json

app = Flask(__name__)

@app.route('/')
def api_root():
	return "Hello World\n"

@app.route('/articles')
def api_articles():
	return 'list of ' + url_for('api_articles') + '\n'

@app.route('/articles/<articleid>') #Can utilize path converters to change data type of articleid if needed with <type:articleid>, default is string.
def api_article(articleid):
	return 'You are reading ' + articleid + '\n'

@app.route('/hello') #Example if browser url is /hello, returns Jane Doe. If browser url has /hello?name=variable, it will return the variable instead.
def api_hello():
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

if __name__ == '__main__':
	app.run(host='0.0.0.0')