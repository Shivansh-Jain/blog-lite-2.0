# from worker import celery
from celery.schedules import crontab
from datetime import datetime,timedelta
from models import Accounts,Posts,Follow,Likes,Comments
from base64 import b64encode
from emails import send_email
from jinja2 import Template
import csv
from app import cache,celery


# from application.helperfunction import monthlyProgress
# from flask import current_app as app
import os
from weasyprint import HTML
import uuid




@celery.task()
def daily_reminders():
        '''
        This will retrive all user and send reminder for their logins
        '''
        list_users = Accounts.query.all()


        yesterday = datetime.now() - timedelta(days=1)
        for user in list_users:
            last_login_time =user.last_login
            if last_login_time > yesterday:
                print('called')
                msg = '''
                Dear {},<br>
                You have not visited Your account since one day,<br>
                Plase, Visit check the recent updates <br>
                <br>
                Thank you<br>
                Blog Lite Team
                '''.format(user.name)
                send_email(user.user_id, "Daily Reminder", msg)

@celery.task()
@cache.memoize(timeout=20)
def create_user_csv_file(user_id:str):
    csv_filds = ['user_id', 'Post title', 'Post containt', 'timestamp', 'Path']
    csv_data = []
    list_posts = Posts.query.filter_by(user_id=user_id)
    # csv_data.append(list_posts)
    for post in list_posts:
        l = [post.user_id, post.title, post.caption, post.timestamp, post.post]
        csv_data.append(l)
    file_name = user_id + ".csv"
    file_path = os.path.join(os.curdir,'static', file_name)
    # csv_file = open(file_name)
    with open(file_path, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(csv_filds)
        csvwriter.writerows(csv_data)
    msg = '''
    Dear {}, <br>
    Please, Find attachment of  your post list <br>
    <br><br>
    Thank you
    Team Blog Lite
    '''
    send_email(user_id, "Custom import Job", msg, file_name)


@celery.task()
def monthly_report(user_id):
        user=Accounts.query.filter_by(user_id=user_id).one()
        all_post=Posts.query.filter_by(user_id=user_id).filter(Posts.timestamp>datetime.now() - timedelta(days=30)).all()
        print(all_post)
        totalpost=len(all_post)

        totallikes=0
        totalcomment=0
        for post in all_post:
             totallikes+=len(post.like_rel)
             totalcomment+=len(post.comment_rel)
        totalfollower=len(user.user_followers)
        totalfollowing=len(user.user_following)

        # print(totalpost,totalfollower,totalfollowing,totalcomment,totallikes)
        filename=month = datetime.today().strftime("%B")+user_id+'.pdf'
        file_path = os.path.join(os.curdir,'static','monthly', filename)

        with open(r"template/monthly.html") as file:
             template_a=Template(file.read())
        with open(r"template/pdfmonthly.html") as file:
             pdf_template= Template(file.read())
        pdf_html= HTML(string=pdf_template.render(name=user.name,month=month,total_follower=totalfollower,total_following=totalfollowing,total_posts=totalpost,
        total_likes=totallikes,total_comment=totalcomment))
        pdf_html.write_pdf(target=file_path)

        send_email(to_address=user_id,subject='Monthly report',message=template_a.render(name=user.name),content='html',attachment_file=file_path)
        return 'success'
        # return(all_post)
        # list_final_post, total_likes, total_comments, total_post_count = monthly_report(user_id)
        # template_file = open("celery_jobs/monthly_report.html")
        # TEMPLATE = template_file.read()
        # template_file.close()
        # template = Template(TEMPLATE)
        # image_labels  = ['Number of Posts', 'Liker', 'Comments']
        # image_data=[total_post_count, total_likes, total_comments]
        # image_name = "barchart.png"
        # plt.bar(image_labels, height=image_data, color=['blue', 'red', 'green'])
        # plt.ylabel(image_name)
        # plt.savefig("barchart.png")
        # with open(image_name, "rb") as image_file:
        #     image_data = image_file.read()
        # image_base64 = b64encode(image_data)
        # message= template.render(user_name = user_name, total_post_count = total_post_count, total_likes=total_likes, total_comments=total_comments, image_base64=image_base64)





@celery.task()
def just_say_hello(name):
    print("INSIDE TASK")
    print('Hello {}'.format(name))
    return 'Hello {}'.format(name)

@celery.task()
def print_current_time_job():
    print("START")
    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string) 
    print("COMPLETE")
    return dt_string