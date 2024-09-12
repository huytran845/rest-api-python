# rest-api-python
### A example framework of a RESTful API using python and flask.

#### Description
The purpose of this project was to demonstrate the basic functionalities and features of a RESTful API with the flask library. This api showcases how the API can send information from GET requests, as well as respond appropriately based on the type of request method needed in a backend call. Additionally, POST requests can be sent back to the server and the API can submit data to the server for processing based on the call. Error handling is showcased in the API as well, where information from a GET request isn't availble, the API will respond with an error 404. Basic authentication is demonstrated through a decorator function that can only be accessed with proper credentials. Lastly, logging is a feature through the imported logging library.

#### How to Run and Install
***This project was made to be demonstrated on the Ubantu environment***
***Make sure you have python 3+ installed***
1.Download the restAPI.py file.
2.Open up a terminal.
3.Enter the command: "sudo pip install flask".
4.Run the program with: "python3 restAPI.py".

#### How to Use The Framework
*Testing root*
curl http://127.0.0.1:5000/

*Testing basic route and variable selection*
curl http://127.0.0.1:5000/articles
curl http://127.0.0.1:5000/articles/123 (Or any value can replace 123, demonstrates that value's selection)

*Testing route provided parameters*
curl http://127.0.0.1:5000/hello_user (no argument provided)
curl http://127.0.0.1:5000/hello_user?name=Joe (Joe provided as argument for name value)

*Testing request methods*
curl -X GET http://127.0.0.1:5000/echo (or just curl http://127.0.0.1:5000/echo because default is GET request)
curl -X POST http://127.0.0.1:5000/echo
curl -X PATCH http://127.0.0.1:5000/echo
curl -X PUT http://127.0.0.1:5000/echo
curl -X DELETE http://127.0.0.1:5000/echo

*Testing data requests and data headers*
curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/messages -d '{"message":"Hello Data"}' (emulates data sent in POST as a JSON)

curl -H "Content-type: application/octet-stream" -X POST http://127.0.0.1:5000/messages --data-binary @message.bin (emulates data sent in POST as a file, which gets written out)

*Viewing response headers*
curl -i http://127.0.0.1:5000/hello

*Error handling demonstration*
curl http://127.0.0.1:5000/users/1 (1 can be replaced with any value, and if it's not in valid range, will result in an error message).

*Testing basic authentication*
curl http://127.0.0.1:5000/secrets (No user information provided, resulting in error message.)
curl -u "admin:secret" http://127.0.0.1:5000/secrets (If "admin" or "secret" is changed authentication will fail because of invalid credentials, resulting in error message.)

*Logging*
curl http://127.0.0.1:5000/logging (Generates an "app.log" file where all the logs are directed, different levels indicate the different type of information from the logs.)