from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# This is the user model used in the database
# Contains the following field:
#	id 			- Primary Key
#	email 		- email used to login
#	password 	- password used to login
#	accountType	- used to differentiate between account types for now
class User(Base):
	__tablename__ = 'users'

	# unique ID given to each user
	id = Column(Integer, primary_key=True)
	# email address to allow for login, must be unique
	email = Column(String(50), unique=True)
	# password for each user
	password = Column(String(50))
	#type of account s = student, p = professor, a = admin
	accType = Column(String(1))

	def __init__(self, email=None, password=None, accType=None):
		self.email = email
		self.password = password
		self.accType = accType

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id

	def __repr__(self):
		return '<User %r>' %(self.name)


# This is the course model used in the database
# Contains the following field:
#	id 					- Primary Key
#	course number 		- course number
#	course name 		- name of the course
#	instructor			- instructor teaching course
#	nEnrolled			- number of enrolled students
class Course(Base):
	__tablename__ = 'courses'

	# unique ID given to each user
	id = Column(Integer, primary_key=True)
	# course number, is unique
	courseNum = Column(String(10), unique=True)
	# name of the course
	courseName = Column(String(50))
	# name of the instructor teaching the course
	instructor = Column(String(100))
	# number of students in the course
	nEnrolled = Column(Integer)

	def __init__(self, courseNum=None, courseName=None, instructor=None, nEnrolled=None):
		self.courseNum = courseNum
		self.courseName = courseName
		self.instructor = instructor
		self.nEnrolled = nEnrolled

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id

	def __repr__(self):
		return '<Course %r>' %(self.name)