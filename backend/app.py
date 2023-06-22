from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Accounts
from flask_restful import Api
from flask_jwt_extended import JWTManager
from api import Accounts_api, Post_api, Follow_api, Like_api, Login_api,api_init,bcrypt,Comments_api
import os
from cache_config import make_cache
from worker import create_celery_inst
# from jobs import export_csv
from flask_cors import CORS

os.curdir
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
print(SQLALCHEMY_DATABASE_URI)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

app.config['SMTP_SERVER_HOST']= "localhost"
app.config['SMTP_SERVER__PORT']= 1025
app.config['SENDER_ADDRESS']= "email@abhishek.com"
app.config['SENDER_PASSWORD']= ""
app.config['REDIS_URL']="redis://localhost:6379"

# app.config['CACHE_TYPE']="RedisCache"
# app.config['CACHE_REDIS_HOST']="localhost"
# app.config['CACHE_REDIS_PORT']=6379
# app.config['CACHE_DEFAULT_TIMEOUT']=300
db.init_app(app)
api=Api(app)
bcrypt.init_app(app)
CORS(app)
jwt = JWTManager(app)



api.add_resource(Accounts_api, '/api/accounts',
                 '/api/accounts/<string:user_id>/<string:search>/<string:all>', '/api/accounts/<string:user_id>')
api.add_resource(Post_api, '/api/posts',
                 '/api/posts/<string:user_id>', '/api/posts/<string:p_id>')
api.add_resource(
    Follow_api, '/api/follow/<string:user_id>/<string:follower>', '/api/follow')
api.add_resource(Like_api, '/api/like', '/api/like/<string:post_id>')
api.add_resource(Login_api,'/api/login')
api.add_resource(Comments_api,'/api/comment','/api/comment/<int:p_id>')

app.app_context().push()
celery = create_celery_inst(app)
app.app_context().push()

cache=make_cache(app)
app.app_context().push()



app.config['SECRET_KEY'] = "starting mission"
app.app_context().push()





# @app.route('/hello/<username>',methods=['GET','POST'])
# def hello(username):
#     job=task.just_say_hello.delay(username)
#     return str(job),200   

# @app.route('/reminder',methods=['GET',"POST"])
# def remind():
#     job=task.daily_reminders.delay()
#     return str(job),200
import task


@app.route('/reminder',methods=['GET',"POST"])
def remind():
    job=task.daily_reminders.delay()
    return str(job),200

@app.route('/csv/<user_id>' ,methods=['GET','POST'])
def call_csv(user_id):
    job=task.create_user_csv_file.delay(user_id)
    return str('success'),200

@app.route('/monthly/<user_id>',methods=["GET","POST"]) 
def report(user_id):
    job=task.monthly_report(user_id)
    return str(job),200

with app.app_context():
    db.create_all()
if __name__ == "__main__":
    app.run(debug=True,port=8000)