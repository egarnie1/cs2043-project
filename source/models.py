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