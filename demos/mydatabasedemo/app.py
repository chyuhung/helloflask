from flask import Flask,flash,redirect,url_for,render_template
from flask_sqlalchemy import SQLAlchemy
import os
import click


app=Flask(__name__)
db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URL','sqlite:///'+os.path.join(app.root_path, 'data.db'))
app.secret_key="12345678"

class Note(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.Text)

@app.cli.command()
def initdb():
    db.create_all()
    click.echo("Initialized Database.")

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, Note=Note) # 等同于{'db': db, 'Note': Note}


@app.route('/index',methods=["GET"])
def index():
    form=DeleteNoteForm()
    notes=Note.query.all()
    return render_template('index.html',notes=notes,form=form)

from forms import NewNoteForm,EditNoteForm
@app.route('/new_note',methods=['GET','POST'])
def new_note():
    form=NewNoteForm()
    if form.validate_on_submit():
        body=form.body.data
        note=Note(body=body)
        db.session.add(note)
        db.session.commit()
        flash("Your note saved successful!")
        return redirect(url_for('index'))
    return render_template('new_note.html',form=form)

@app.route('/edit_note/<int:note_id>',methods=['GET','POST'])
def edit_note(note_id):
    form=EditNoteForm()
    note=Note.query.get(note_id)
    if form.validate_on_submit():
        note.body=form.body.data
        db.session.commit()
        flash("Edit successful!")
        return redirect(url_for("index"))
    form.body.data=note.body
    return render_template('edit_note.html',form=form)

from forms import DeleteNoteForm
from flask import abort
@app.route('/delete_note/<int:note_id>',methods=['POST'])
def delete_note(note_id):
    form=DeleteNoteForm()
    if form.validate_on_submit():
        note=Note.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        flash('Delete successful!')
    else:
        abort("400")
    return redirect(url_for("index"))