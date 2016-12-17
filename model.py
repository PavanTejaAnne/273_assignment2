from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)
DATABASE = 'newtest'
PASSWORD = 'pavan'
USER = 'root'
HOSTNAME = 'localhost'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)
db=SQLAlchemy(app)

class Orders(db.Model):
    __tablename__='Order'
    id=db.Column('Id',db.Integer, primary_key=True)
    Name=db.Column('Name',db.String(80))
    Email=db.Column('Email',db.String(50))
    Category=db.Column('Category',db.String(50))
    Description = db.Column('Description', db.String(250))
    link = db.Column('Link', db.String(300))
    estimated_cost = db.Column('Estimated_cost', db.String(300))
    submit_date = db.Column('Submit_date', db.String(100))
    decision_date = db.Column('DECISION_DATE',db.String(100))
    status = db.Column('Status', db.String(20))
    

    def __init__(self, Name, Email, Category, Description, link, estimated_cost, submit_date, status, decision_date):
        self.Name=Name
        self.Email=Email
        self.Category=Category
        self.Description=Description
        self.link=link
        self.estimated_cost=estimated_cost
        self.submit_date=submit_date
        self.decision_date=decision_date
        self.status=status

class CreateDB():
    def __init__(self, hostname=None):
        engine = sqlalchemy.create_engine('mysql://%s:%s@%s' % (USER, PASSWORD, HOSTNAME))
        engine.execute("CREATE DATABASE IF IT DOES NOT EXIST %s " % (DATABASE)) 
        db.create_all()
