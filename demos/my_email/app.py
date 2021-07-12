# -*- coding: utf-8 -*-

from flask_mail import Mail,Message
from flask import Flask
import os

app=Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '123456789')
#随着配置逐渐增多，改用app.config 对象的update（）方法来加载配置
#在实例化Mail 类时，flask-mail会获取配置以创建一个用于发信的对象，所以确保在实例化Mail 类之前加载配置
app.config.update(
    MAIL_SERVER='smtp.163.com',
    MAIL_PORT=25,
    MAIL_USERNAME='15023765237@163.com',
    MAIL_PASSWORD='OQGAGTEOYDNEJXRX',
    MAIL_DEFAULT_SENDER='15023765237@163.com>'
)

mail = Mail(app)


def send_mail(to,subject,body):
    message=Message(subject=subject,recipients=[to],body=body)
    mail.send(message)

from forms import Sendmail
from flask import render_template,redirect,url_for
@app.route('/index',methods=['post','get'])
def index():
    form=Sendmail()
    if form.validate_on_submit():
        to=form.to.data
        subject=form.subject.data
        body=form.body.data
        send_mail(to,subject,body)
        return redirect(url_for('index'))
    return render_template('index.html',form=form)
