from app import app, db
from sqlalchemy.orm import backref
from hashlib import md5
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class Rating(db.Model):
	__tablename__ = 'ratingtable'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
	rating = db.Column(db.Float)

	user = db.relationship('User', backref=backref("book_ratings"))
	book = db.relationship('Book', backref=backref("user_ratings"))

	def __init__(self, user=None, book=None, rating=None):
		print "in __init__: ", user, book, rating
		self.user = user
		self.book = book
		self.rating = rating

	def __repr__(self):
		return '<User %r, Book %r, Rating %r>' % (self.user.username,
					self.book.name, self.rating)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), index=True, unique=True)
	password_hash = db.Column(db.String(100))
	email = db.Column(db.String(120), index=True, unique=True)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)
	followed = db.relationship('User', secondary=followers, 
								primaryjoin=(followers.c.follower_id == id), 
								secondaryjoin=(followers.c.followed_id == id), 
								backref=db.backref('followers', lazy='dynamic'), 
								lazy='dynamic')
	books = db.relationship('Book', secondary='ratingtable', lazy='dynamic')

	def __init__(self, username, password, email):
		self.username = username
		self.password_hash = pwd_context.encrypt(password)
		self.email = email

	def generate_auth_token(self, expiration=600):
		s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
		return s.dumps({ 'id': self.id })

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None #valid token, but expired
		except BadSignature:
			return None #invalid token
		user = User.query.get(data['id'])
		return user

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)
			
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return True

	def get_id(self):
		return unicode(self.id)

	def avatar(self, size):
		#from gravatar
		return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def followed_posts(self):
		return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

	def ratedValue(self, bookid):
		rating = 0.0
		ratings = self.book_ratings
		for r in ratings:
			if r.book.id == int(bookid):
				rating = r.rating
		
		print "Rating is{}".format(rating)
		return "{}".format(rating)
		

	def add_book_rating(self, user, book, rating):
		print user, book, rating
		ratings_for_user = self.book_ratings
		for r in ratings_for_user:
			if r.book == book:
				print "Found existing rating"
				r.rating = rating
				db.session.commit()
				return self

		ratingObject = Rating(user=user, book=book, rating=rating)
		db.session.add(ratingObject)
		self.book_ratings.append(ratingObject)
		db.session.commit()
		return self

	def __repr__(self):
		return '<User %r>' % (self.username)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post %r>' %(self.body)


class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(140))
	author = db.Column(db.String(100))
	isbn = db.Column(db.String(20))
	url = db.Column(db.String(140))
	users = db.relationship('User', secondary='ratingtable', lazy='dynamic')

	def __init__(self, name, author, isbn, url):
		self.name = name
		self.author = author
		self.isbn = isbn
		self.url = url
		
	def __repr__(self):
		return '<Book %r>' %(self.name)

