import os
import sys
import time
import subprocess
from subprocess import run
from random import randrange
import json
import wtforms
import random
import string
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_from_directory
from collections import defaultdict
import math
from jinja2 import Environment, meta
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired
import datetime
import string
from werkzeug import secure_filename
import requests
from flask.ext.classy import FlaskView
from flask import abort, redirect, flash
import itsdangerous
# from itsdangerous import URLSafeSerializer, BadSignaturew
import locale




APPLICATION_NAME='Picto'
app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'Insert_random_string_here'
app.secret_key = 'bla bla bla?'#secret session
app.config['ALLOWED_EXTENSIONS'] = set(['zip'])



# def get_serializer(secret_key=None):
#     if secret_key is None:
#         secret_key = app.secret_key
#     return URLSafeSerializer(secret_key)








def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/register', methods=('GET', 'POST'))
def submit():
	global row
	global column
	global	type_
	form = Myform()
	if form.validate_on_submit():
		row = request.form['row']
		column = request.form['column']
		type_ = request.form['type_']
		return redirect('/')
	return render_template('input.html', form=form)





class  Myform(Form):
    row = TextField('row', validators=[DataRequired()])
    column = TextField('column',validators=[DataRequired()])
    type_ = TextField('type_ ',validators=[DataRequired()])






@app.route('/')
def index():
    return render_template('index.html')






@app.route('/upload', methods=['POST','GET'])
# def decode():
# 	global link
# 	encoding = locale.getdefaultlocale()[1]
# 	cmd = subprocess.Popen('pwd',shell=True,stdout=subprocess.PIPE)
# 	for line in cmd.stdout:
# 		link = line.decode(encoding).split()
	

def upload():
	file = request.files['file']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		run('mkdir %s'%(file.filename)).stdout
		app.config['UPLOAD_FOLDER'] = '%s' % (file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		run('unzip %s/*zip -d %s'%(filename,filename)).stdout
		run('montage %s/*.%s -tile %sx%s  %s.pdf '%(filename,type_,row,column,filename)).stdout
		run('mv  %s.pdf static/images'%(filename)).stdout
		global link
		encoding = locale.getdefaultlocale()[1]
		cmd = subprocess.Popen('pwd',shell=True,stdout=subprocess.PIPE)
		for line in cmd.stdout:
  			link = line.decode(encoding).split()
  			if link:
  				print(link[-1])
		global test

		test = ('images/%s.pdf' %(filename))
		# test= ('/static/images/logo.png')
		flash (test[0:50])
		return redirect(url_for('Downloadpage'))
	elif file or not allowed_file(file.filename):
		return redirect(url_for('Errorpage'))






# @app.route('/upload/download/<payload>')
# def Downloadpage(payload):
#     s = get_serializer()
#     try:
#         user_id = s.loads(payload)
#     except BadSignature:
#         abort(404)

#     user = User.query.get_or_404(user_id)
#     user.activate()
#     flash('User activated')
#     return redirect(url_for('index'))




@app.route('/static/')
def Downloadpage(filename=None):
	return render_template('success.html')


@app.route('/upload/error')
def Errorpage(filename=None):
    return render_template('error.html')






##webserver
if __name__ == '__main__':
	app.debug = True
	app.run(host='localhost',port=5000)