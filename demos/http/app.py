# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import json
import os

import click

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from jinja2 import escape
from jinja2.utils import generate_lorem_ipsum
from flask import Flask, make_response, request, redirect, url_for, abort, session, jsonify

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')



#自定义命令
@app.cli.command('hello')
def test():
    click.echo('this is a test')

# get name value from query string and cookie
# @app.route('/hello')
# def hello():
#     name = request.args.get('name')
#     if name is None:
#         name = request.cookies.get('name', 'Human')
#     response = '<h1>Hello, %s!</h1>' %name
#     #response ='<h1>my number is %s</h1>' %escape(telnum)  # escape name to avoid XSS
#     # return different response according to the user's authentication status
#     if 'logged_in' in session:
#         response += '[Authenticated]'
#     else:
#         response += '[Not Authenticated]'
#     return response



# redirect
@app.route('/hi')
def hi():
    return redirect(url_for('hello'))


# use int URL converter
@app.route('/goback/<int:year>')
def go_back(year):
    return 'Welcome to %d!' % (2018 - year)

#use int URL converter
@app.route('/goto/<int:year>')
def goto(year):
    return 'welcome to %d'%(2020+year)


# use any URL converter
colors=['blue','white','dark','red','green','yellow']
@app.route('/colors/<any(%s):color>'%str(colors)[1:-1])
def three_colors(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'


# return error response
@app.route('/brew/<drink>')
def teapot(drink):
    if drink == 'coffee':
        abort(418)
    else:
        return 'A drop of tea.'


# 404
@app.route('/404')
def not_found():
    abort(404)


# return response with different formats
@app.route('/note', defaults={'content_type': 'text'})
@app.route('/note/<content_type>')
def note(content_type):
    content_type = content_type.lower()
    if content_type == 'text':
        body = '''Note
to: Peter
from: Jane
heading: Reminder
body: Don't forget the party!
'''
        response = make_response(body)
        response.mimetype = 'text/plain'
    elif content_type == 'html':
        body = '''<!DOCTYPE html>
<html>
<head></head>
<body>
  <h1>Note</h1>
  <p>to: Peter</p>
  <p>from: Jane</p>
  <p>heading: Reminder</p>
  <p>body: <strong>Don't forget the party!</strong></p>
</body>
</html>
'''
        response = make_response(body)
        response.mimetype = 'text/html'
    elif content_type == 'xml':
        body = '''<?xml version="1.0" encoding="UTF-8"?>
<note>
  <to>Peter</to>
  <from>Jane</from>
  <heading>Reminder</heading>
  <body>Don't forget the party!</body>
</note>
'''
        response = make_response(body)
        response.mimetype = 'application/xml'
    elif content_type == 'json':
        body = {"note": {
            "to": "Peter",
            "from": "Jane",
            "heading": "Remider",
            "body": "Don't forget the party!"
        }
        }
        response = jsonify(body)
        # equal to:
        # response = make_response(json.dumps(body))
        # response.mimetype = "application/json"
    else:
        abort(400)
    return response


# set cookie
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


# log in user
@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))


# protect view
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page.'


# log out user
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


# AJAX
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more',
            type: 'get',
            success: function(data){
                $('.body').append(data);
            }
        })
    })
})
</script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)


# redirect to last page
@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' \
           % url_for('do_something', next=request.full_path)

@app.route('/test')
def test():
    response=make_response('this is a test')
    response.mimetype='text/plain'
    return response

@app.route('/test01')
def test01():
    data={
        'name':'chyuhung',
        'number':'77777'
    }
    response=make_response(json.dumps(data))
    response.mimetype='application/json'
    return response


from flask import jsonify
@app.route('/test02')
def test02():
    return jsonify(name='chyuhung',num='7')


from flask import Flask,make_response
@app.route('/test03/<name>')
def test03(name):
    response=make_response(redirect(url_for('hello')))
    response.set_cookie('name',name)
    return response

from flask import redirect,session,url_for
@app.route('/logintest')
def logintest():
    session['logged_in']=True
    return redirect(url_for('hellotest'))

@app.route('/admintest')
def admintest():
    if 'logged_in' not in session:
        abort(403)
    return 'YES'

from flask import session,request
@app.route('/hellotest')
def hellotest():
    name=request.args.get('name')
    if name is None:
        name=request.cookies.get('name','xixi')
    response='<h1>hello,%s</h1>'%name
    if "logged_in" in session:
        response +='YES'
    else:
        response +='NO'
    return response

@app.route('/logouttest')
def logouttest():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hellotest'))


@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something and redirect</a>' \
           % url_for('do_something', next=request.full_path)


@app.route('/do-something')
def do_something():
    # do something here
    return redirect_back()


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc



@app.route('/tztest01')
def tztest01():
    response='there is test01,goto tztest03:<a href="%s">tztest03</a>'%url_for('tztest03')
    return response

@app.route('/tztest02')
def tztest02():
    response='there is test02,goto tztest03:<a href="%s">tztest03</a>'%url_for('tztest03')
    return response

@app.route('/tztest03')
def tztest03():
    #do something
    return  redirect(request.referrer or url_for('hellotest'))

@app.route('/tztest04')
def tztest04():
    response='there is test04,goto tztest05:<a href="%s">tztest05</a>'%url_for('tztest03',next=request.full_path)
    return response

@app.route('/tztest05')
def tztest05():
    #do something
    return redirect(request.args.get('next'))


def redirect_back(default='hellotest', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

@app.route('/dos')
def dos():
    #do something
    return redirect_back()

@app.route('/dostest')
def dostest():
    response = '<a href="%s">goto dos</a>' % url_for('dos', next=request.full_path)
    return response


@app.route('/posttest')
def posttest():
    post_body=generate_lorem_ipsum(n=2)#生成两段随机文本
    return '''
    <h1>a very long post</h1>
    <div class="body">%s</div>
    <button id="load">load more</button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
    $(function(){
        $('#load').click(function(){
            $.ajax({
                url:'/moretest',            //目标URL
                type:'get',             //请求方法
                success:function(data){ //返回2xx响应后触发的回调函数
                $('.body').append(data);//将返回的响应插入页面中
                }
            })
        })
    })
    </script>
    '''%post_body

@app.route('/moretest')
def moretest():
    return generate_lorem_ipsum(n=1)

from jinja2 import escape
@app.route('/escapetest')
def escapetest():
    name=request.args.get('name')
    return "<h1>hello,%s</h1>"%escape(name)

