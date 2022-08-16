#!/usr/bin/env python
import sys
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
import pymysql.cursors
import cgitb
import cgi
import sys
import math
import ldap
import settings # Our server and db settings, stored in settings.py
cgitb.enable()

app = Flask(__name__, static_url_path='/static')
# Set Server-side session config: Save sessions in the local app directory.
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
Session(app)

####################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Bad request' } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Resource not found' } ), 404)

####################################################################################
#
# Routing: GET, DELETE, POST using Flask-Session
#
class SignIn(Resource):
	#
	# Login, start a session and set/return a session cookie
	#
	def post(self):
		if not request.json:
			abort(400) # bad request
		# Parse the json
		parser = reqparse.RequestParser()
 		try:
 			# Check for required attributes in json document, create a dictionary
	 		parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		# Already logged in
		if request_params['username'] in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			try:
				l = ldap.open(settings.LDAP_HOST)
				l.start_tls_s()
				l.simple_bind_s("uid="+request_params['username']+
					", ou=People,ou=fcs,o=unb", request_params['password'])
				# At this point we have sucessfully authenticated.

				session['username'] = request_params['username']
				response = {'status': 'success' }
				responseCode = 201
			except ldap.LDAPError, error_message:
				response = {'status': 'Access denied'}
				responseCode = 403
			finally:
				l.unbind()

		return make_response(jsonify(response), responseCode)

	# GET: Check for a login
	#
	def get(self):
		success = False
		if 'username' in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403

		return make_response(jsonify(response), responseCode)

	# DELETE: Logout: remove session
	#
	def delete(self):
		
		if 'username' in session:
			session.clear()
		else:
			response = {'status': 'No Cookie Found'}
			responseCode = 404

		return make_response(jsonify(response), responseCode)

####################################################################################
#
# POST and GET for ToDoList
#
class ToDoList(self):
    #get the to do list
    def get(self):

        #if the user doesn't exist return 404
        if 'username' in session:
            response = {'status': 'User does not exist'}
	    responseCode = 404
	
	

	sql = "call getToDoList("[user]")"

        try:
            #open the connection, call the stored procedure
	    dbConnection = pymysql.connect(settings.DB_HOST,
			    settings.DB_USER,
			    settings.DB_PASSWD,
			    settings.DB_DATABASE,
			    charset='utf8mb4',
			    cursorclass= pymysql.cursors.DictCursor)
            cursor = dbConnection.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                print("<tr><td> {toDoString}</td>, <td>{isDone}</td></tr>".format(**row) )

            #close the connection
            cursor.close()
            dbConnection.close()

        except pymysql.MySQLError as e:
            print("<p>Ooops - Things messed up: </p>")

	response = {'status': 'List retrived Successfully'}
        return make_response(jsonify(response), 200)
    def post(self, text):
	
	if not request.json or not 'toDoString' in request.json:
            abort(400) # bad request

	#if the user doesn't exist return 404
        if 'username' in session:
            response = {'status': 'User does not exist'}
	    responseCode = 404
	
	# The request object holds the ... wait for it ... client request!
        # Pull the results out of the json request
	toDo = request.json['toDoString'];

	sql = "call addToDo("[user]", "toDo")"

        try:
	    dbConnection = pymysql.connect(settings.DB_HOST,
			    settings.DB_USER,
			    settings.DB_PASSWD,
			    settings.DB_DATABASE,
			    charset='utf8mb4',
			    cursorclass= pymysql.cursors.DictCursor)
            cursor = dbConnection.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                print("<tr><td> {toDoString}</td>, <td>{isDone}</td></tr>".format(**row) )

            cursor.close()
            dbConnection.close()

        except pymysql.MySQLError as e:
            print("<p>Ooops - Things messed up: </p>")

        response = {'status': 'List Item Added Successfully'}
        return make_response(jsonify(response), 200)

####################################################################################
#
# PUT, DELETE, and GET for ToDoList
#
class ToDoListResource(self):
# GET: Return identified school resource
#
    def get(self):

	 #if the user doesn't exist return 404
        if 'username' in session:
            response = {'status': 'User does not exist'}
	    responseCode = 404
	

	sql = "call getToDoList("[user]", "[toDoID]")"

        try:
            #open the connection, call the stored procedure
	    dbConnection = pymysql.connect(settings.DB_HOST,
			    settings.DB_USER,
			    settings.DB_PASSWD,
			    settings.DB_DATABASE,
			    charset='utf8mb4',
			    cursorclass= pymysql.cursors.DictCursor)
            cursor = dbConnection.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                print("<tr><td> {toDoString}</td>, <td>{isDone}</td></tr>".format(**row) )

            #close the connection
            cursor.close()
            dbConnection.close()

        except pymysql.MySQLError as e:
            print("<p>Ooops - Things messed up: </p>")

	response = {'status': 'List Item retrived Successfully'}
        return make_response(jsonify(response), 200)


    def put(self):
		
	if not request.json or not 'toDoString' in request.json:
            abort(400) # bad request

        #if the user doesn't exist return 404
        if 'username' in session:
            response = {'status': 'User does not exist'}
	    responseCode = 404

	# The request object holds the ... wait for it ... client request!
        # Pull the results out of the json request
	newText = request.json['toDoString'];

	sql = "call changeToDoText("[user]", "[toDoID]", "newText")"

        try:
	   dbConnection = pymysql.connect(settings.DB_HOST,
			    settings.DB_USER,
			    settings.DB_PASSWD,
			    settings.DB_DATABASE,
			    charset='utf8mb4',
			    cursorclass= pymysql.cursors.DictCursor)
            cursor = dbConnecion.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                print("<tr><td> {toDoString}</td>, <td>{isDone}</td></tr>".format(**row) )

            cursor.close()
            dbConnection.close()

        except pymysql.MySQLError as e:
            print("<p>Ooops - Things messed up: </p>")

        response = {'status': 'List Item Text Changed Successfully'}
        return make_response(jsonify(response), 200)
	#call the method to delete an item in the list
    def delete(self, toDoID):

        #if the user doesn't exist return 404
        if 'username' in session:
            response = {'status': 'User does not exist'}
	    responseCode = 404

	sql = "call deleteToDo("[user]", "[toDoID]")"

        try:
	   dbConnection = pymysql.connect(settings.DB_HOST,
			    settings.DB_USER,
			    settings.DB_PASSWD,
			    settings.DB_DATABASE,
			    charset='utf8mb4',
			    cursorclass= pymysql.cursors.DictCursor)
            cursor = dbConnecion.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()

            cursor.close()
            dbConnection.close()

        except pymysql.MySQLError as e:
            print("<p>Ooops - Things messed up: </p>")

        response = {'status': 'List Item Deleted Successfully'}
        return make_response(jsonify(response), 200)      

####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(SignIn, '/signin')
api.add_resource(Users,'/users')
api.add_resource(User,'/users/<string: user>')
api.add_resource(ToDoList,'/users/<string: user>/todo')
api.add_resource(ToDoListResource, '/users/<string: user>/todo/<int:toDoID>')


#############################################################################
# xxxxx= last 5 digits of your studentid. If xxxxx > 65535, subtract 30000
if __name__ == "__main__":
   	app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.APP_DEBUG)
