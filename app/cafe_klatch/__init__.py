from flask import Flask,url_for
#from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os



app = Flask(__name__)

app.secret_key = 'development key'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:jasmeet@localhost/mysql'

engine = create_engine('mysql://root:jasmeet@localhost/mysql')
#Session = sessionmaker(bind=engine) 
#dbsession = Session()

from models import db
db.init_app(app)
 
import cafe_klatch.routes