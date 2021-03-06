import sys
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import Course, User, Base
from forms import LoginForm, CreateUserForm, CreateCourseForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'TOTALLYNOTSECRET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:\\University\\Year2\\Fall\\CS2043\\Project\\source\\database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Clear the database and create three new users
@app.before_first_request
def setup():
	print("Setup")
	Base.metadata.drop_all(bind=db.engine) 	
	Base.metadata.create_all(bind=db.engine)
	db.session.add(User('student@unb.ca', 'password123', 's'))
	db.session.add(User('prof@unb.ca', 'password123', 'p'))
	db.session.add(User('admin@unb.ca', 'password123', 'a'))
	db.session.add(Course('CS2043', 'Software Engineering 1', 'Dr. Jong-Kyou Kim', 3))
	db.session.add(Course('CS2263', 'Systems Software Development', 'Dr. Jeffrey McNally', 6))
	db.session.add(Course('CS1083', 'Java 2', 'Dr. Josee Tasse', 9))
	db.session.commit()

@login_manager.user_loader
def loadUser(userId):
	return db.session.query(User).get(int(userId))

# Main index
@app.route('/')
def index():
	return render_template('index.html')

# Error page when there is an error authenticating
@app.route('/error')
def error():
	return render_template('error.html')

# Allows users to login into dashboard
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = db.session.query(User).filter_by(email=form.email.data).first()
		if user:
			if user.password == form.password.data:
				login_user(user, remember=form.remember.data)
				app.logger.info("User " + form.email.data + " logged in")
				return redirect(url_for('dashboard'))

		return redirect(url_for('error'))
	
	return render_template('login.html', form=form)

# Page for admins to create a new user
@app.route('/newUser', methods=['GET', 'POST'])
@login_required
def newUser():
	form = CreateUserForm()

	if form.validate_on_submit():
		if form.accountType.data != 'a' or form.accountType.data != 'p' or form.accountType.data != 's':
			db.session.add(User(form.email.data, form.password.data, form.accountType.data))
			db.session.commit()
			app.logger.info("New User " + form.email.data + " registered")
			return redirect(url_for('dashboard'))

		return redirect(url_for('error'))
	
	return render_template('newUser.html', form=form)

# Page for admins to create a new course
@app.route('/newCourse', methods=['GET', 'POST'])
@login_required
def newCourse():
	form = CreateCourseForm()

	if form.validate_on_submit():
		db.session.add(Course(form.courseNum.data, form.courseName.data, form.instructor.data, 0))
		db.session.commit()
		app.logger.info("New Course " + form.courseNum.data + " registered")
		return redirect(url_for('dashboard'))
	
	return render_template('newCourse.html', form=form)

# Redirects a user to their appropriate dashboard
@app.route('/dashboard')
@login_required
def dashboard():
	if current_user.accType == 'a':
		return redirect(url_for('admindashboard'))
	elif current_user.accType == 's':
		return redirect(url_for('studentdashboard'))
	elif current_user.accType == 'p':
		return redirect(url_for('profdashboard'))

# Admin dashboard
@app.route('/admindashboard')
@login_required
def admindashboard():
	courses = db.session.query(Course).all()
	students = db.session.query(User).all()
	return render_template('admindashboard.html', email=current_user.email, courseList=courses, studentList=students)

# Student dashboard
@app.route('/studentdashboard')
@login_required
def studentdashboard():
	courses = db.session.query(Course).all()
	return render_template('studentdashboard.html', email=current_user.email, courseList=courses)

# Professor dashboard
@app.route('/profdashboard')
@login_required
def profdashboard():
	return render_template('profdashboard.html', email=current_user.email)

# Logs out user
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

if __name__ == '__main__':
	if sys.argv[1] == "reset":
		setup()
	app.run(debug=True)