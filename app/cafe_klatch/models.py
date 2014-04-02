from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
 
db = SQLAlchemy()
 
class Blocked_Chat_Users(db.Model):
    __tablename__ = 'blocked_chat_users'

    id =db.Column(db.Integer)
    Blocker =db.Column(db.String(50),primary_key=True)
    Blocked =db.Column(db.String(50),primary_key=True)
    Status =db.Column(db.Integer)

    def __init__(self, myid, Blocker, Blocked,status):
        
        self.id = myid
        self.Blocker = Blocker
        self.Blocked = Blocked
        self.Status = status
        



class Peer_UserStatus_Model(db.Model):
    __tablename__ = 'peer_userstatus'

    username = db.Column(db.String(30), primary_key = True)
    #date = db.Column(db.String(100))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    verfication_code = db.Column(db.String(10))
    isVerified = db.Column(db.Integer)
    

    def __init__(self, username, email, password,verfication_code,isVerified):
        self.username = username        
        self.email = email
        self.set_password(password)
        self.verfication_code = verfication_code
        self.isVerified = isVerified

    def set_password(self, password):
        self.password = password#generate_password_hash(password)

    def check_password(self, password):
        return self.password#check_password_hash(self.password, password)

class User_Info_Model(db.Model):
    __tablename__ = 'user_info'

    userid = db.Column(db.String(30), primary_key = True)
    fullname = db.Column(db.String(50))
    bday =db.Column(db.DateTime)
    country = db.Column(db.String(30))
    zipcode = db.Column(db.String(7))
    gender = db.Column(db.String(1))
    heightinches = db.Column(db.Integer)
    zodiac = db.Column(db.String(15))
    smoke = db.Column(db.String(1))
    drink = db.Column(db.String(1))
    diet= db.Column(db.String(1))
    marital = db.Column(db.String(1))
    c1_nature = db.Column(db.String(300))
    c1_never = db.Column(db.String(300))
    heightfeet = db.Column(db.Integer)
    c1_friday = db.Column(db.String(150))
    c1_mostimp = db.Column(db.String(150))
    c1_life = db.Column(db.String(300))
    c1_friends = db.Column(db.String(300))
    c2_food = db.Column(db.String(150)) 
    c2_movies = db.Column(db.String(150))
    c2_books = db.Column(db.String(150))
    c2_sports = db.Column(db.String(150))
    c2_tour = db.Column(db.String(150))
    c2_hangout = db.Column(db.String(300))
    c3_marriage = db.Column(db.String(300))
    c3_love = db.Column(db.String(300)) 
    c3_parenthood = db.Column(db.String(300))
    c3_honesty = db.Column(db.String(300)) 
    c3_world = db.Column(db.String(300)) 
    c3_pets = db.Column(db.String(300))
    imagename = db.Column(db.String(50)) 
    status = db.Column(db.String(10))
     
    def __init__(self, userid,  status):
        self.userid = userid        
        self.status = status
        self.imagename="default.png"
        self.gender="M"

class Peer_Chat1(db.Model):

    __tablename__ = 'peer_chat'  
    
    id = db.Column(db.Integer(), primary_key = True)
    From = db.Column(db.String(255))
    To = db.Column(db.String(30))
    message = db.Column(db.Text())
    sent = db.Column(db.DateTime)
    recd = db.Column(db.Integer)
    sex = db.Column(db.String(5))
    stratus = db.Column(db.Text())
    action = db.Column(db.Integer)
    online = db.Column(db.Integer)

    def __init__(self, From,To, message,sent,action,recd=0,sex='M',stratus="",online=0 ):
        self.From = From
        self.To = To
        self.message = message
        self.sent =sent
        self.recd =recd
        self.sex = sex
        self.stratus = stratus
        self.action = action
        self.online = online        
