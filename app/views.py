# views.py

#############
## imports ##
#############

from flask import Flask, flash, redirect, render_template, request, session, url_for
from functools import wraps
from forms import AddTaskForm, RegisterForm, LoginForm
from flask.ext.sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.exc import IntegrityError

##############
##  config  ##
##############

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import Task, User

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	session.pop('user_id', None)
	session.pop('role', None)
	flash('You are logged out. Bye! :(')
	return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			u = User.query.filter_by(
				name=request.form['name'],
				password=request.form['password']
			).first()
			if u is None:
				error = 'Invalid username or password.'
				return render_template(
					"login.html",
					form=form,
					error=error
				)
			else:
				session['logged_in'] = True
				session['user_id'] = u.id
				session['role'] = u.role
				flash('You are logged in. Go Crazy!')
				return redirect(url_for('tasks'))
		else:
			return render_template(
				"login.html",
				form=form,
				error=error
			)
	if request.method == 'GET':
		return render_template('login.html', form=form)

# this function is here to facilitate displaying existing tasks
@app.route('/tasks/')
@login_required
def tasks():
	open_tasks = db.session.query(Task) \
		.filter_by(status='1').order_by(Task.due_date.asc())

	closed_tasks = db.session.query(Task) \
		.filter_by(status='0').order_by(Task.due_date.asc())

	return render_template(
		'tasks.html',
		form=AddTaskForm(request.form),
		open_tasks=open_tasks,
		closed_tasks=closed_tasks
	)

# function for adding a new task
@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_task():
	form = AddTaskForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_task = Task(
				form.name.data,
				form.due_date.data,
				form.priority.data,
				datetime.datetime.utcnow(),
				'1',
				session['user_id']
			)
			db.session.add(new_task)
			db.session.commit()
			flash('New entry was successfully posted. Thanks.')
		else:
			flash('Invalid Entry.  Please try again.')
	return redirect(url_for('tasks'))


# function for marking a task as complete
@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
	new_id = task_id
	task = db.session.query(Task).filter_by(task_id=new_id).update({"status":"0"})
	if session['user_id'] == task.first().user_id or session['role'] == "admin":
		task.update({"status:" "0"})
		db.session.commit()
		flash('The task was marked as complete. Nice.')
		return redirect(url_for('tasks'))
	else:
		flash('You can only update tasks that belong to you.')
		return redirect(url_for('tasks'))

# function for handling entry deletion
@app.route('/delete/<int:task_id>/',)
@login_required
def delete_entry(task_id):
	new_id = task_id
	task = db.session.query(Task).filter_by(task_id=new_id).delete()
	if session['user_id'] == task.first().user_id or session['role'] == "admin":
		task.delete()
		db.session.commit()
		flash('The task was deleted.')
		return redirect(url_for('tasks'))
	else:
		flash('You can only delete tasks that belong to you.')
		return redirect(url_for('tasks'))

def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			flash(u"Error in the %s field -%s" % (
				getattr(form, field).label.text, error), 'error')

# function for handling user registration
@app.route('/register/', methods=['GET', 'POST'])
def register():
	error = None
	form = RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_user = User(
				form.name.data,
				form.email.data,
				form.password.data,
			)
			try:
				db.session.add(new_user)
				db.session.commit()
				flash('Thanks for registering.  Pleaes login.')
				return redirect(url_for('login'))
			except IntegrityError:
				error = 'Oh no! That username and/or email already exist. Please try again.'
				return render_template('register.html', form=form, error=error)
		else:
			return render_template('register.html', form=form, error=error)
	if request.method == 'GET':
		return render_template('register.html', form=form)


# function for creating admin user
def create_admin_user(self):
	new_user = User(
		name='Superman',
		email='admin@realpython.com',
		password='allpowerfull',
		role='admin'
	)
	db.session.add(new_user)
	db.session.commit()








