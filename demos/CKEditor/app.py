from flask import Flask,render_template,url_for,flash,redirect
from flask_ckeditor import CKEditor
from forms import RichTextForm


app=Flask(__name__)
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.secret_key='abcdefg'
ckeditor=CKEditor(app)

@app.route("/ckeditor",methods=['POST','GET'])
def ckeditor():
    form=RichTextForm()
    if form.validate_on_submit():
        if form.save.data:
            flash("Save successful!")
        elif form.publish.data:
            flash("Publish successful!")
        return redirect(url_for('index'))
    return render_template('richtextform.html',form=form)

@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html')


from forms import SignForm,RegisterForm
#登录和注册app
@app.route('/login',methods=['GET','POST'])
def login():
    sign_form=SignForm()
    register_form=RegisterForm()

    if sign_form.signin.data and sign_form.validate_on_submit():
        flash('Sign successful!')
        return redirect(url_for('index'))
    if register_form.register.data and register_form.validate_on_submit():
        flash('Register successful!')
        return redirect(url_for('index'))
    return render_template('login.html',sign_form=sign_form,register_form=register_form)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error))


#仅渲染表单
@app.route('/xr_login')
def xr_login():
    sign_form=SignForm()
    register_form=RegisterForm()
    return render_template('login.html',sign_form=sign_form,register_form=register_form)

#仅处理表单
@app.route('/handle_signin',methods=['POST'])
def handle_signin():
    sign_form=SignForm()
    if sign_form.validate_on_submit():
        flash('Sign in !')
        return redirect(url_for('index'))
    return render_template('index.html',sign_form=sign_form)

@app.route('/handle_register',methods=['POST'])
def handle_register():
    register_form=RegisterForm()
    if register_form.validate_on_submit():
        flash('Register !')
        return redirect(url_for('index'))
    return render_template('index.html',register_form=register_form)