from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import click

app=Flask(__name__)

# #Flask-SQLAlchemy建议设置SQLALCHEMY_TRACK_MODIFICATIONS配置变量，
# #这个配置变量决定是否追踪对象的修改，这用于Flask-SQLAlchemy的事件通知系统。
# #这个配置键的默认值为None，如果没有特殊需要，可以把它设为False来关闭警告信息。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("DATABASE_URL","sqlite:///"+os.path.join(app.root_path,"data.db"))
app.secret_key="chyuhung"

db=SQLAlchemy(app)
migrate=Migrate(app,db) #在db对象创建后调用

# #使用app.shell_context_processor装饰器注册一个shell上下文处理函数
@app.shell_context_processor
def make_shell_context():
    return dict(db=db,
                # Author=Author,Article=Article,Writer=Writer,Book=Book,Singer=Singer,Song=Song,
                #City=City,Citizen=Citizen,Country=Country,Capital=Capital
                Student=Student,Teacher=Teacher
           )

# #初始化数据库
# #实现一个自定义flask命令完成数据库初始化
@app.cli.command()
@click.option("--drop",is_flag=True,help="Create after drop.")
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm("This operation will delete the database,do you want to continue?",abort=True)
        db.drop_all()
        click.echo("Drop tables.")
    db.create_all()
    click.echo("Initialized Database.")

association_table=db.Table("association",db.Column("student_id",db.Integer,db.ForeignKey("student.id")),db.Column("teacher_id",db.Integer,db.ForeignKey("teacher.id")))

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),unique=True)
    grade=db.Column(db.String(20))
    teachers=db.relationship("Teacher",secondary=association_table,back_populates="students")

class Teacher(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),unique=True)
    office=db.Column(db.String(20))
    students=db.relationship("Student",secondary=association_table,back_populates="teachers")


#
# class Author(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(70),unique=True)
#     phone=db.Column(db.String(20))
#     articles=db.relationship("Article")
#     # optional
#     def __repr__(self):
#         return '<%r>' % self.name
#
# class Article(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     title=db.Column(db.String(50),index=True)
#     body=db.Column(db.Text)
#     author_id=db.Column(db.Integer,db.ForeignKey('author.id'))
#     # optional
#     def __repr__(self):
#         return '<%r>' % self.title
#
# class Writer(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(70),unique=True)
#     books=db.relationship("Book",back_populates="writer")
#     # optional
#     def __repr__(self):
#         return '<%r>' % self.name
#
# class Book(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     title=db.Column(db.String(50),index=True)
#     body=db.Column(db.Text)
#     writer_id=db.Column(db.Integer,db.ForeignKey("writer.id"))
#     writer=db.relationship("Writer",back_populates="books")
#     # optional
#     def __repr__(self):
#         return '<%r>' % self.title
#
# class Singer(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(20))
#     songs=db.relationship("Song",backref="singer")
#
#     def __repr__(self):
#         return "<%r>" %self.name
#
# class Song(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     title=db.Column(db.String(50))
#     singer_id=db.Column(db.Integer,db.ForeignKey("singer.id"))
#
#     def __repr__(self):
#         return "<%r>" %self.title
#
# class Citizen(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(20))
#     city_id=db.Column(db.Integer,db.ForeignKey("city.id"))
#     city=db.relationship("City")
#
#     def __repr__(self):
#         return "<%r>"%self.name
#
# class City(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(30))
#     def __repr__(self):
#         return "<%r>" %self.name
#
# class Country(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), unique=True)
#     capital = db.relationship('Capital', back_populates='country', uselist=False)
#
# class Capital(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), unique=True)
#     country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
#     country = db.relationship('Country', back_populates='capital', )
