from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import datetime


class Accounts(db.Model):

    __tablename__="accounts"
    user_id=db.Column(db.String,primary_key=True)
    password=db.Column(db.String,nullable=False)
    name=db.Column(db.String,nullable=False)
    profile=db.Column(db.String,nullable=False)
    last_login=db.Column(db.DateTime, nullable= False)
    user_posts=db.relationship('Posts',uselist=True,cascade='delete',foreign_keys='Posts.user_id',backref=db.backref('post_rel'))
    user_followers=db.relationship('Follow',cascade='delete',foreign_keys='Follow.user',backref=db.backref('user_rel'))
    user_following=db.relationship('Follow',cascade='delete',foreign_keys='Follow.following',backref=db.backref('following_rel'))
    user_likes=db.relationship('Likes',cascade='delete',foreign_keys='Likes.user_id',backref=db.backref('Likes_rel'))
    user_comments=db.relationship('Comments',cascade='delete',foreign_keys='Comments.user_id',backref=db.backref('Comments_rel'))
    def get_id(self):
            return (self.user_id)

class Posts(db.Model):
    __tablename__='posts'
    user_id=db.Column(db.String,db.ForeignKey("accounts.user_id"),nullable=False)
    post_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    post=db.Column(db.String,nullable=False)
    caption=db.Column(db.String)
    title=db.Column(db.String,nullable=False)
    timestamp=db.Column(db.DateTime,default=datetime.datetime.now())
    like_rel=db.relationship('Likes',uselist=True,foreign_keys='Likes.post_id',cascade='delete')
    comment_rel=db.relationship('Comments',uselist=True,foreign_keys='Comments.post_id',cascade='delete')

class Likes(db.Model):
    __tablename__='likes'
    l_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    post_id=db.Column(db.Integer,db.ForeignKey("posts.post_id"))
    user_id=db.Column(db.String,db.ForeignKey('accounts.user_id'))
    
class Comments(db.Model):
     __tablename__ = "comments"
     c_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
     post_id=db.Column(db.Integer,db.ForeignKey("posts.post_id"))
     user_id=db.Column(db.String,db.ForeignKey("accounts.user_id"))
     comment=db.Column(db.String,nullable=False) 

   
class Follow(db.Model):
    __tablename__="following"
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    user=db.Column(db.String,db.ForeignKey("accounts.user_id"))
    following=db.Column(db.String,db.ForeignKey("accounts.user_id"))

