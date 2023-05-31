from . import dbsql
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired ,DataRequired ,FileAllowed
from wtforms import StringField , SubmitField ,TextAreaField ,PasswordField,EmailField,FormField,IntegerField,SelectField , FloatField
from wtforms.validators import EqualTo, Length , NumberRange
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField

SLUG_CHOICES = [('1','Yüz Tanıma'),('2','Ses Tanıma'),('3','Yapay Zeka'),('4','İnternet Bilgi Sistemi'),('5','Chat Bot'),('6','Ev Otomasyonu'),('7','Güvenlik Sistemleri'),('8','Eğlence'),('9','Diğer..')]
class SpotifyUsername(dbsql.Model):
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    data = dbsql.Column(dbsql.String(10000))
    date = dbsql.Column(dbsql.DateTime(timezone=True), default=func.now())
    user_id = dbsql.Column(dbsql.Integer, dbsql.ForeignKey('user.id'))
    

class SpotifyEmail(dbsql.Model):
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    data = dbsql.Column(dbsql.String(10000))
    date = dbsql.Column(dbsql.DateTime(timezone=True), default=func.now())
    user_id = dbsql.Column(dbsql.Integer, dbsql.ForeignKey('user.id'))
    

class SpotifyPassword(dbsql.Model):
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    data = dbsql.Column(dbsql.String(10000))
    date = dbsql.Column(dbsql.DateTime(timezone=True), default=func.now())
    user_id = dbsql.Column(dbsql.Integer, dbsql.ForeignKey('user.id'))
    
class NetflixEmail(dbsql.Model):
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    data = dbsql.Column(dbsql.String(10000))
    date = dbsql.Column(dbsql.DateTime(timezone=True), default=func.now())
    user_id = dbsql.Column(dbsql.Integer, dbsql.ForeignKey('user.id'))
    

class NetflixPassword(dbsql.Model):
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    data = dbsql.Column(dbsql.String(10000))
    date = dbsql.Column(dbsql.DateTime(timezone=True), default=func.now())
    user_id = dbsql.Column(dbsql.Integer, dbsql.ForeignKey('user.id'))
    
class UserInformation(dbsql.Model):
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    spotify_username= dbsql.Column(dbsql.String(150))
    spotify_email= dbsql.Column(dbsql.String(150), )
    spotify_password= dbsql.Column(dbsql.String(150))
    netflix_email= dbsql.Column(dbsql.String(150))
    netflix_password=dbsql.Column(dbsql.String(150))
    date = dbsql.Column(dbsql.DateTime(timezone=True), default=func.now())
    user_id = dbsql.Column(dbsql.Integer, dbsql.ForeignKey('user.id'))

class Messages(dbsql.Model):
    id = dbsql.Column(dbsql.Integer , primary_key = True)
    name = dbsql.Column(dbsql.String(255))
    email = dbsql.Column(dbsql.String(255))
    subject = dbsql.Column(dbsql.String(255))
    message = dbsql.Column(dbsql.Text)
    sender_id = dbsql.Column(dbsql.Integer, dbsql.ForeignKey('user.id'))


class Posts(dbsql.Model):
    id = dbsql.Column(dbsql.Integer , primary_key = True)
    title = dbsql.Column(dbsql.String(255))
    content = dbsql.Column(dbsql.Text)
    date_posted = dbsql.Column(dbsql.DateTime , default=datetime.utcnow)
    slug = dbsql.Column(dbsql.String(255))
    poster_id = dbsql.Column(dbsql.Integer, dbsql.ForeignKey('user.id'))

class ShoppingCart(dbsql.Model):
    id = dbsql.Column(dbsql.Integer , primary_key = True)
    product = dbsql.Column(dbsql.String(255))
    quantity = dbsql.Column(dbsql.Integer)
    date_added = dbsql.Column(dbsql.DateTime , default=datetime.utcnow)
    price = dbsql.Column(dbsql.Integer)
    buyer = dbsql.Column(dbsql.Integer)
    shopper_id = dbsql.Column(dbsql.Integer,dbsql.ForeignKey('user.id'))
    
class Products(dbsql.Model):
    id = dbsql.Column(dbsql.Integer , primary_key = True)
    name= dbsql.Column(dbsql.String(255),nullable = False)
    price = dbsql.Column(dbsql.Numeric(precision=10, scale=2),nullable = False)
    discount = dbsql.Column(dbsql.Integer,default = 0)
    stock = dbsql.Column(dbsql.Integer,nullable = False)
    date_added = dbsql.Column(dbsql.DateTime , default=datetime.utcnow)
    description = dbsql.Column(dbsql.Text,nullable= False)
    image_1 = dbsql.Column(dbsql.String(255),nullable=True,default = 'image.jpeg')
    image_2 = dbsql.Column(dbsql.String(255),nullable=True,default = 'image.jpeg')
    image_3 = dbsql.Column(dbsql.String(255),nullable=True,default = 'image.jpeg')

class AddProduct(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    price = FloatField('Price',validators=[DataRequired()])
    stock = IntegerField("Stock",validators=[DataRequired()])
    discount = IntegerField("Discount",default = 0)
    description =  TextAreaField("Description", validators=[DataRequired()])
    image_1 = FileField("Image 1", validators=[ FileAllowed(['jpg','png','gif','jpeg'])])
    image_2 = FileField("Image 2", validators=[ FileAllowed(['jpg','png','gif','jpeg'])])
    image_3 = FileField("Image 3", validators=[ FileAllowed(['jpg','png','gif','jpeg'])])
    submit = StringField("Submit")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField('Content',validators=[DataRequired()])
    author = StringField("Author")
    """ slug =  StringField("Slug", validators=[DataRequired()]) """
    slug = SelectField('Slug' , choices=SLUG_CHOICES ,validators=[DataRequired()])
    submit = StringField("Submit")

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    spotify_username = StringField("spotify_username")
    spotify_email = EmailField("spotify_email")
    spotify_password = StringField("spotify_password")
    netflix_email = EmailField("netflix_email")
    netflix_password = StringField("netflix_password")
    about_author = TextAreaField("About Author")
    profile_pic = FileField("Profile Pic")
    submit = SubmitField("Submit")

class User(dbsql.Model, UserMixin):
    id = dbsql.Column(dbsql.Integer, primary_key=True)
    email = dbsql.Column(dbsql.String(150), unique=True)
    password = dbsql.Column(dbsql.String(150))
    name = dbsql.Column(dbsql.String(150))
    username = dbsql.Column(dbsql.String(20), unique=True)
    date_added = dbsql.Column(dbsql.DateTime , default=datetime.utcnow)
    about_author = dbsql.Column(dbsql.Text(), nullable=True)
    profile_pic = dbsql.Column(dbsql.String(), nullable=True)
    stock_limit = dbsql.Column(dbsql.Integer , nullable = True,default = 0)
    Spotify_Username=dbsql.Column(dbsql.String(150), nullable=True)
    Spotify_Email=dbsql.Column(dbsql.String(150), nullable=True)
    Spotify_Password=dbsql.Column(dbsql.String(150), nullable=True)
    Netflix_Email=dbsql.Column(dbsql.String(150), nullable=True)
    Netflix_Password=dbsql.Column(dbsql.String(150), nullable=True) 
    spotify_username=dbsql.relationship('SpotifyUsername')
    spotify_email=dbsql.relationship('SpotifyEmail')
    spotify_password=dbsql.relationship('SpotifyPassword')
    netflix_email=dbsql.relationship('NetflixEmail')
    netflix_password=dbsql.relationship('NetflixPassword')
    user_information=dbsql.relationship('UserInformation')
    messages = dbsql.relationship('Messages')
    posts = dbsql.relationship('Posts' ,backref='poster')
    shopping_cart = dbsql.relationship('ShoppingCart' ,backref = 'shopper')
    def __repr__(self):
        return '<Name %r>' % self.username
