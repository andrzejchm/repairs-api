from flask import request
from flask_api import FlaskAPI
from app.controllers.login import postLogin

###

def create_app():
	app = FlaskAPI(__name__)
	
	@app.route('/auth/login')
	def login():
		return { 'obj': request.data }
		
	return app
