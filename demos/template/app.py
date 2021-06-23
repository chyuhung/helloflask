import os
from flask import render_template,Flask,url_for,Markup,flash,redirect
app=Flask(__name__)
app.secret_key=os.getenv('SECRET_KEY','scret string')
app.jinja_env.trim_blocks=True
app.jinja_env.lstrip_blocks=True


user={'username':'chyuhung',
      'bio':'a boy who loves movies and music'
      }

movies=[{'name':'this is a movies name','year':'2020'},
        {'name':'this is new movies name','year':'2019'},
        {'name':'this is old movies name','year':'2018'},
        {'name':'this is the last movies name','year':'2012'}]

@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html',user=user,movies=movies)

@app.route('/')
def index():
    return render_template('index.html')

#上下文装饰器
@app.context_processor
def inject_foo():
    foo="I am foo"
    return dict(foo=foo)#等同于rerurn {'foo':'foo'}

@app.route('/flash')
def just_flash():
    flash("welcome!")
    return redirect(url_for('watchlist'))

def musical(s):
    return s +Markup('&#9835;')
app.jinja_env.filters['musical']=musical

def baz(n):
    if n == 'baz':
        return True
    else:
        return  False
app.jinja_env.tests['baz']=baz

def bar():
    return "I am bar"
foo="I am foo"
app.jinja_env.globals['bar']=bar
app.jinja_env.globals['foo']=foo


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404