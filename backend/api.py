from flask import Flask, request
from flask_restful import Api, Resource, marshal_with, fields, marshal
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from models import Accounts, Posts, Follow, Likes,Comments
from models import db
import os
from datetime import datetime as dt
import datetime

from flask import current_app as app
api_init = Api()
bcrypt = Bcrypt()
# CORS(app)


class Login_api(Resource):
    def post(self):
        user_id = request.get_json()['user_id']
        print(user_id)
        password = request.get_json()['password']
        user = Accounts.query.filter_by(user_id=user_id).first()
        time=dt.now()
        print(user)
        print(bcrypt.check_password_hash(user.password,password))
        if user is None or not bcrypt.check_password_hash(user.password, password):
            return {'status': False, 'msg': 'User ID or Password is incorrect.'}
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(
            identity=user_id, expires_delta=expires)
        user.last_login=time
        db.session.commit()
        return {'status': True, 'access_token': access_token,"username":user.name}, 200


class Accounts_api(Resource):
    output = {"user_id": fields.String,
              "password": fields.String,
              "name": fields.String,
              "profile": fields.String}

    # @marshal_with(output)
    def get(self, user_id, search, all):
        output = {"user_id": fields.String,
                  "password": fields.String,
                  "name": fields.String,
                  "profile": fields.String}
        if search == "False" and all == 'False':
            user = Accounts.query.filter_by(user_id=user_id).first()
            if user:
                return {'status': True, 'accounts': marshal(user, output)}, 200
            return '', 404
        elif all == 'True':
            return Accounts.query.all()
        else:
            print("else")
            user = Accounts.query.filter(
                Accounts.name.ilike('%'+user_id+'%')).all()
            print(user)
            return {'status': True, 'accounts': marshal(user, output)}, 200

    # @marshal_with(output)
    def post(self):
        print('called')
        name = request.form['name']
        user_id = request.form['user_id']
        password = request.form['password']
        image = request.files.get('profile')
        # data = request.get_json()
        # print(data)
        if not Accounts.query.filter_by(user_id=user_id).first():
            hpassword = bcrypt.generate_password_hash(password)
            location = os.path.join(
                os.getcwd(),'..', 'blog-lite', 'src', 'assets', 'profile', user_id+'.jpg')
            image.save(
                location)
            path = os.path.join('..', 'assets', 'profile'+user_id+'.jpg')
            user = Accounts(user_id=user_id, name=name,
                            password=hpassword, profile=path,last_login=dt.now())
            
            db.session.add(user)
            db.session.commit()
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(
                identity=user_id, expires_delta=expires)
            return {'status': True, 'access_token': access_token}, 200
        return {'status': False, 'message': 'Username already exists'}, 401

    def put(self):
        name = request.form['name']
        user_id = request.form['user_id']
        password = request.form['password']
        image = request.files.get('profile')
        hpassword = bcrypt.generate_password_hash(password)
        user = Accounts.query.filter_by(user_id=user_id).first()
        path=os.getcwd()+'/blog-lite\/src\/assets\/profile/'+user_id+'.jpg'
        if image:
            os.remove(path)
            image.save(path)
        user.name=name
        user.password=hpassword
        db.session.commit()
        return '',200

    def delete(self, user_id):
        posts = Posts.query.filter_by(user_id=user_id).all()
        p=os.getcwd()+'/blog-lite\/src\/assets\/posts/'
        for post in posts:
            path = os.path.join(p, post.post)
            os.remove(path)
        p=os.getcwd()+'/blog-lite\/src\/assets\/profile/'
        path = os.path.join(p, user_id+'.jpg')
        os.remove(path)
        element = Accounts.query.filter_by(user_id=user_id).first()
        db.session.delete(element)
        db.session.commit()
        return '',200
# api.add_resource(Accounts_api, "/api/login",'/api/accounts')
# api.add_resource(Accounts_api, )


class Post_api(Resource):
    output = {'post_id': fields.String,
              'post': fields.String,
              'title': fields.String,
              'caption': fields.String,
            #   'timestamp': fields.String,
              'timestamp': fields.String(attribute=lambda x: x.timestamp.strftime('%d-%m-%Y %I:%M %p')),
              'path': fields.String,
              'user_id': fields.String,
              'name': fields.String(attribute=lambda x: x.post_rel.name),
              'liked_by': fields.Raw(attribute=lambda x: [i.user_id for i in x.like_rel])
              }

    @jwt_required()
    def post(self):
        # data = request.get_json()
        user_id=get_jwt_identity()
        # print(current_user)
        print('entered')
        # user_id="login@gmail.com"
        image=request.files.get('image')
        print('entered')
        title=request.form['title']

        print('entered')
        caption=request.form['caption']
        print('entered')
        timestamp=datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        name=timestamp+user_id+image.filename
        location = os.path.join(
                os.getcwd(),'..', 'blog-lite', 'src', 'assets', 'posts',name)
        image.save(location)
        # path = os.path.join('..', 'assets', 'posts'+name)
        post = Posts(post=name, title=title, caption=caption, timestamp=dt.now(), user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return {'status':True}

    @marshal_with(output)
    @jwt_required()
    def get(self,user_id):
        current_user=get_jwt_identity()
        # print(current_user)
        if user_id == '0':
            data = Posts.query.all()
        else: 
        
            data = Posts.query.filter_by(user_id=user_id).all()

        data = sorted(data, key=lambda x: x.timestamp, reverse=True)
        return data

    def put(self):
        data = request.get_json()
        post = Posts.query.filter_by(post_id=data.get('post_id')).first()
        post.timestamp=dt.now()
        post.title = data.get('title')
        post.caption = data.get('caption')
        db.session.commit()
        return "", 200

    def delete(self, user_id):
        post = Posts.query.filter_by(post_id=int(user_id)).first()
        location = os.path.join(
                os.getcwd(),'..', 'blog-lite', 'src', 'assets', 'posts',post.post)
        os.remove(location)
        db.session.delete(post)
        db.session.commit()
        return 200


class Follow_api(Resource):
    output = {
        'user': fields.String,
        'following': fields.String,
        'names': fields.String(attribute=lambda x: x.user_rel.name),
        'fnames': fields.String(attribute=lambda x: x.following_rel.name)
    }
    @jwt_required()
    def post(self):
        print("follow")
        data = request.get_json()
        print('data',data)
        user=get_jwt_identity()
        follow = Follow(user=user, following=data.get('following'))
        db.session.add(follow)
        db.session.commit()
        return "", 201

    # @marshal_with(output)
    def get(self, user_id, follower):
        output = {
        'user': fields.String,
        'following': fields.String,
        'names': fields.String(attribute=lambda x: x.user_rel.name),
        'fnames': fields.String(attribute=lambda x: x.following_rel.name)
    }
        if follower == "True":
            data = Follow.query.filter_by(following=user_id).all()

        else:
            data = Follow.query.filter_by(user=user_id).all()
        print(data)
        return {'status': True, 'accounts': marshal(data, output)}, 200

    @jwt_required()
    def delete(self):
        data = request.get_json()
        user=get_jwt_identity()
        Follow.query.filter_by(user=user, following=data.get('following')).delete()

        db.session.commit()
        return 200


class Like_api(Resource):
    output = {
        'post_id': fields.Integer,
        'user_id': fields.String
    }

    @marshal_with(output)
    def get(self):
        data = Likes.query.all()
        return data, 200
    @jwt_required()
    def post(self):
        user_id=get_jwt_identity()
        data = request.get_json()
        like = Likes(post_id=data.get('id'), user_id=user_id)
        db.session.add(like)
        db.session.commit()
        return 200

    def delete(self):
        data = request.get_json()
        Likes.query.filter_by(post_id=data.get(
            'id'), user_id=data.get('user')).delete()
        db.session.commit()
        return 200


class Comments_api(Resource):
    output = {
        'user_id':fields.String,
        'name': fields.String(attribute=lambda x: x.Comments_rel.name),
        'comment':fields.String
    }
    @marshal_with(output)
    @jwt_required()
    def get(self,p_id):
        comments = Comments.query.filter_by(post_id=p_id).all()
        return comments
    # @jwt_required()
    def post(self): 
        print('called')
        # print(request.)
        print(request.get_json()) 
        data=request.get_json()
        print(data['user_id'])
        entry=Comments(post_id=data.get('post_id'),user_id=data.get('user_id'),comment=data.get('comment'))
        db.session.add(entry)
        db.session.commit()
        return 200