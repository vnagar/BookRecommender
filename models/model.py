from app import db
from hashlib import md5

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class Rating(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
	rating = db.Column(db.Float)

	user = db.relationship('User', backref='ratings')
	book = db.relationship('Book', backref='ratings')

	def __init__(self, user=None, book=None, rating=None):
		self.user = user
		self.book = book
		self.rating = rating

	def __repr__(self):
		return '<User %r, Book %r, Rating %r>' % (self.user.username,
					self.book.name, self.rating)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), index=True, unique=True)
	password = db.Column(db.String(20))
	email = db.Column(db.String(120), index=True, unique=True)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)
	followed = db.relationship('User', secondary=followers, 
								primaryjoin=(followers.c.follower_id == id), 
								secondaryjoin=(followers.c.followed_id == id), 
								backref=db.backref('followers', lazy='dynamic'), 
								lazy='dynamic')
	books = db.relationship('Book',
								secondary="rating",
								lazy='dynamic')

	def __init__(self , username ,password , email):
		self.username = username
		self.password = password
		self.email = email

	def verify_password(self, password):
		if password == self.password:
			return True
		return False
			
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

	def add_book_rating(self, book, rating):
		self.ratings.append(Rating(user=self, book=book, rating=rating))
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
	users = db.relationship('User',
								secondary='rating',
								lazy='dynamic')

	def __init__(self, name, author, isbn, url):
		self.name = name
		self.author = author
		self.isbn = isbn
		self.url = url
		
	def __repr__(self):
		return '<Book %r>' %(self.name)
