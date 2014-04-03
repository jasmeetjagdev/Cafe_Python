#from cafe_klatch import dbsession
from cafe_klatch import app
from werkzeug import secure_filename
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, IntegerField, validators, ValidationError,PasswordField, DateField,SelectField, RadioField,FileField
from models import db, Peer_UserStatus_Model,User_Info_Model,Peer_Chat1,Blocked_Chat_Users
from flask import session,jsonify,Response,json
import operator
import datetime,json,time 
from sqlalchemy import create_engine
import os,math
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")
  
class SignupForm(Form):
    username = TextField("UserID",  [validators.Required("Please enter your Username.")])
    email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = Peer_UserStatus_Model.query.filter_by(username = self.username.data).first()
        if user:
            self.email.errors.append("That UserID is already taken")
            return False
        else:
            return True

class EditProfileForm(Form):
    #userid  = TextField("UserId")
    
    fullname= TextField("Full Name") 
    country= TextField("Country")
    bday = DateField("Birthday")
    zipcode = TextField("Zip Code")
    gender = RadioField("Gender",choices = [('M','Male'),('F','Female')])
    heightinches = SelectField(u'Height Inches',choices = [(x,y) for x in range(10) for y in range(10) if x==y], coerce = int )
    zodiac = SelectField(u'Zodiac',choices = [('1','Leo'),('2','Virgo'),('3','Aquarius'),('4','Aries'),('5','Scorpio'),('6','Capricorn'),('7','Sagittarius'),('8','Taurus'),('9','Pisces'),('10','Cancer')] )
    smoke = SelectField("Smoke",choices = [('Y','Yes'),('N','No')])
    drink = SelectField("Drink",choices = [('N','Not at all'),('R','Rarely'),('S','Socially'),('O','Very Often')])
    diet = SelectField("Diet",choices = [('V','Vegetarian'),('N','Non-Vegetarian')])
    marital = SelectField("Martial",choices = [('S','Single'),('L','Seeing Someone'),('M','Married')])
    c1_nature = TextAreaField("My nature")
    c1_never = TextAreaField("5 Things I could never do without")
    heightfeet = SelectField(u'Height Inches',choices = [('3','3'),('4','4'),('5','5'),('6','6'),('7','7')], coerce = int )
    c1_friday = TextAreaField("5 places for spending Friday Nights")
    c1_mostimp = TextAreaField("5 Most important things in my life ")
    c1_life = TextAreaField("For me life is")
    c1_friends = TextAreaField("For me friends are")
    c2_food = TextAreaField("Food")
    c2_movies = TextAreaField("Movies")
    c2_books = TextAreaField("Books")
    c2_sports = TextAreaField("Sports")
    c2_tour = TextAreaField("Tourist spots")
    c2_hangout = TextAreaField("Hangouts with friends")
    c3_marriage = TextAreaField("About Marriage")
    c3_love = TextAreaField("Love at First sight")
    c3_parenthood = TextAreaField("About Parenthood")
    c3_honesty = TextAreaField("About Honesty")
    c3_world = TextAreaField("About an ideal world")
    c3_pets = TextAreaField("Keeping pets")
    status  =  TextField("Status")
    image = FileField("Image")
    
    submit = SubmitField("Edit Profile")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def load_from_DB(self,request):
        username=session['userid']
        nuser = User_Info_Model.query.filter_by(userid=username).first()
        self.imagename=nuser.imagename
        
        self.fullname.data   = nuser.fullname
        self.country.data    = nuser.country
        self.bday.data       = nuser.bday
        self.zipcode.data    = nuser.zipcode
        self.gender.data     = nuser.gender
        self.heightinches.data= nuser.heightinches
        self.zodiac.data      = nuser.zodiac
        self.smoke.data       = nuser.smoke
        self.drink.data       = nuser.drink
        self.diet.data        = nuser.diet
        self.marital.data     = nuser.marital
        self.c1_nature.data   = nuser.c1_nature
        self.c1_never.data    = nuser.c1_never
        self.heightfeet.data  = nuser.heightfeet
        self.c1_friday.data   = nuser.c1_friday
        self.c1_mostimp.data  = nuser.c1_mostimp
        self.c1_life.data     = nuser.c1_life
        self.c1_friends.data  = nuser.c1_friends
        self.c2_food.data     = nuser.c2_food
        self.c2_movies.data   = nuser.c2_movies
        self.c2_books.data    = nuser.c2_books
        self.c2_sports.data   = nuser.c2_sports
        self.c2_tour.data     = nuser.c2_tour
        self.c2_hangout.data  = nuser.c2_hangout
        self.c3_marriage.data = nuser.c3_marriage
        self.c3_love.data     = nuser.c3_love
        self.c3_parenthood.data= nuser.c3_parenthood
        self.c3_honesty.data  = nuser.c3_honesty
        self.c3_world.data    = nuser.c3_world
        self.c3_pets.data     = nuser.c3_pets
       # self.image.data.filename = nuser.imagename
        
    def saveAll_ExceptImage(self,request):
        username=session['userid']
        nuser = User_Info_Model.query.filter_by(userid=username).first()
        nuser.fullname=self.fullname.data
        nuser.marital = self.marital.data      
        nuser.country = self.country.data  
        nuser.bday    = self.bday.data
        nuser.zipcode = self.zipcode.data    
        nuser.gender  = self.gender.data   
        nuser.heightinches = self.heightinches.data     
        nuser.zodiac = self.zodiac.data    
        nuser.smoke  = self.smoke.data   
        nuser.drink  = self.drink.data   
        nuser.diet   = self.diet.data  
        nuser.marital  = self.marital.data   
        nuser.c1_nature  = self.c1_nature.data   
        nuser.c1_never   = self.c1_never.data  
        nuser.heightfeet = self.heightfeet.data    
        nuser.c1_friday  = self.c1_friday.data   
        nuser.c1_mostimp = self.c1_mostimp.data    
        nuser.c1_life   = self.c1_life.data  
        nuser.c1_friends = self.c1_friends.data    
        nuser.c2_food  = self.c2_food.data   
        nuser.c2_movies = self.c2_movies.data    
        nuser.c2_books  = self.c2_books.data   
        nuser.c2_sports = self.c2_sports.data    
        nuser.c2_tour = self.c2_tour.data    
        nuser.c2_hangout = self.c2_hangout.data    
        nuser.c3_marriage = self.c3_marriage.data    
        nuser.c3_love = self.c3_love.data    
        nuser.c3_parenthood = self.c3_parenthood.data    
        nuser.c3_honesty  = self.c3_honesty.data   
        nuser.c3_world  = self.c3_world.data   
        nuser.c3_pets  = self.c3_pets.data   
        #nuser.image = secure_filename(form.image.data.filename)
        db.session.commit()

    

    def saveImage(self,request):
        # username=session['userid']
        # nuser = User_Info_Model.query.filter_by(userid=username).first()
        # nuser.imagename= secure_filename(self.image.data.filename)
        # session['imagename']= nuser.imagename
        # print "myfilename",self.image.data
        # db.session.commit()
        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
        username=session['userid']
        nuser = User_Info_Model.query.filter_by(userid=username).first()
        #return
        #photos = UploadSet('static/uploads', IMAGES)

        file = request.files['imgfile']
        if not len(file.filename) == 0 :
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
                filename = session['userid']+"."+file.filename.rsplit('.', 1)[1]
                path = os.path.join(os.getcwd(),'cafe_klatch/static/uploads')
                if not os.path.exists(path):
                    os.makedirs(path)            
                file.save(os.path.join(path,filename))
               
                nuser.imagename=filename
                session['imagename']= nuser.imagename
                self.imagename=filename
                db.session.commit()


class MessagesForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user=None

    
    def loadMessages(self):
        engine = create_engine('mysql://root:jasmeet@localhost/mysql')
        connection = engine.connect()
        result1 = connection.execute("Select `from` from (Select * FROM peer_chat WHERE `to` ='"+session['userid']+"' ) as T")
        result2 = connection.execute("Select `to` from (Select * FROM peer_chat WHERE `from` ='"+session['userid']+"' ) as T")
        results = []
        results.append(result1)
        results.append(result2)
        
        result_fin = []
        
        for result in result1:
            for row in result:
                result_fin.append(row)
            

        for result in result2:
            for row in result:
                result_fin.append(row)
        
        self.result_fin =  list(set(result_fin))
        connection.close()
        

class LoginForm(Form):
    #email = TextField("Email",  [validators.Required("Please enter your email address"), validators.Email("Invalid email address !!")])
    username = TextField("UserID",  [validators.Required("* UserID is required !")])
    password = PasswordField('Password', [validators.Required("* Password is required !")])
    submit = SubmitField("Login")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user=None

    def validate(self):
        if not Form.validate(self):
            return False
        
        user = Peer_UserStatus_Model.query.filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('Invalid UserID')
            return False

        if not (user.check_password(self.password.data) == self.password.data):
            self.password.errors.append('Invalid password')
            return False

        if not user.isVerified == 1:
            self.password.errors.append('User Not Verified ! ')
            return False

        self.user = user
        return True

class MatchesForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user=None

    def loadMatches(self):
        #if not Form.validate(self):
        #    return False
        
        user =db.session.query(User_Info_Model).filter(
            User_Info_Model.userid ==(session['userid'])).first()
        session['imagename']=user.imagename

        self.matches =db.session.query(User_Info_Model).filter(
            User_Info_Model.userid !=user.userid,User_Info_Model.gender != user.gender).all()
      

        self.row_match={} # structure (row: %match)
        match=0
        counter=0
        for m in self.matches:
            match=match+self.calculateMatch(user.country,m.country,5)
            match=match+self.calculateMatch_height(user.heightfeet,user.heightinches,m.heightfeet,m.heightinches)
            match=match+self.calculateMatch(user.zodiac,m.zodiac,5)
            match=match+self.calculateMatch(user.smoke,m.smoke,5)
            match=match+self.calculateMatch(user.drink,m.drink,5)
            match=match+self.calculateMatch(user.diet,m.diet,5)
            match=match+self.calculateMatch(user.marital,m.marital,5)
            match=match+self.calculateMatch(user.c1_never,m.c1_never,5)
            match=match+self.calculateMatch(user.c1_friday,m.c1_friday,5)
            match=match+self.calculateMatch(user.c1_mostimp,m.c1_mostimp,5)
            match=match+self.calculateMatch(user.c2_food,m.c2_food,10)
            match=match+self.calculateMatch(user.c2_movies,m.c2_movies,10)
            match=match+self.calculateMatch(user.c2_books,m.c2_books,10)
            match=match+self.calculateMatch(user.c2_sports,m.c2_sports,10)
            match=match+self.calculateMatch(user.c2_tour,m.c2_tour,5)
            match=match+self.calculateMatch(user.c2_hangout,m.c2_hangout,5) 
            
            blockeduser = Blocked_Chat_Users.query.filter_by(Blocker=session['userid'],Blocked=m.userid,Status=0).first()
            nonVerifiedUser =  Peer_UserStatus_Model.query.filter_by(username=m.userid,isVerified=0).first()
            
            if blockeduser is None and nonVerifiedUser is None:
                counter+=1
                self.row_match[m]=match
                match=0
            if counter == 6:
                break
                
        self.rsorted_matches = sorted(self.row_match.iteritems(), key=operator.itemgetter(1),reverse=True)
    
    def calculateMatch(self,user,target,weight):
        if user is None:
            return 1
        if target is None:
            return 2

        user = user.replace( ", ",",")
        user = user.replace( " ,",",")
        user = user.replace( ",","$")
        target = target.replace( ", ",",")
        target = target.replace( " ,",",")
        target = target.replace( ",","$")

        userlist = user.split('$')
        targetlist = target.split('$')

        if (len(userlist)==1 and '' in userlist):
            return 1
        if (len(targetlist)==1 and '' in targetlist):
            return 1

        matches=0;
        totalcount = len(userlist) + len(targetlist);
        
        for x in userlist:
            if x in targetlist:
                matches=matches+1
       
        returnValue =  int(math.ceil(2*matches*weight/totalcount))
        return returnValue
    

    def calculateMatch_height(self,userheightfeet,userheightinches,targetheightfeet,targetheightinches):
        if userheightfeet is None or userheightinches is None or targetheightfeet is None or targetheightinches is None :
            return 1

        if userheightfeet == targetheightfeet:
            if abs(userheightinches - targetheightinches)<=2:
                return 5        
            else:
                return 3
        else :
            if abs(userheightinches - targetheightinches) >=10:
                return 5        
            else:
                return 3
        return 5


class ViewProfileForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user=None

    def loadProfile(self):
        #if not Form.validate(self):
        #    return False
        
        self.user = User_Info_Model.query.filter_by(userid=session['userid']).first()


class ChatForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user=None

    def chatHeartbeat(self,request): 
        results = Peer_Chat1.query.filter_by(To=session['userid'], recd=0).order_by(Peer_Chat1.id)

        items = []

        chatBoxes = []

        for chatters in results:
            if chatters.From not in session['openChatBoxes']:
                if chatters.From in session['chatHistory']:
                    items= items+session['chatHistory'][chatters.From]
            if chatters.action == 0:                
                chatters.message = chatters.message.replace( "\r","")
                chatters.message = chatters.message.replace( "\n","<br>")
            if chatters.action == 1:
                webcam = "code not written "

            items.append({ 's': 0,'f':chatters.From,'m':chatters.message});


            if chatters.From not in session['chatHistory']:
                session['chatHistory'][chatters.From]=[];

            session['chatHistory'][chatters.From].append({ 's': 0,'f':chatters.From,'m':chatters.message});
    
            if 'tsChatBoxes' in session:
                if chatters.From in session['tsChatBoxes']:
                    del session['tsChatBoxes'][chatters.From]
            
            session['openChatBoxes'][chatters.From] = chatters.sent
        
        for box,time1 in session['openChatBoxes'].items():
            if box not in session['tsChatBoxes']:
                now1 = 181 #datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")-time.strptime(time1, "%y-%m-%d %H:%M:%S")
                message = "Sent at "+ str(time1)
                if now1 > 180 :
                    items.append({ 's': 2,'f':box,'m':message});
                    if box not in session['chatHistory']:
                        session['chatHistory'][box]=[];

                    session['chatHistory'][box].append({ 's': 0,'f':box,'m':message}); 

                    session['tsChatBoxes'][box] = 1

        for result in results:
            result.recd = 1
            db.session.commit()
        #alert("itemsBeat"+items);
        mydata = {'items': items}
        self.response=Response(json.dumps(mydata,separators=(',',':')),  mimetype='application/json')

    def sendChat(self,request): 
        chatfrom = session['userid']        
        chatto = request.args.get('to');
        chatmessage = request.args.get('message')
        chataction = request.args.get('action')
        
        session['openChatBoxes'][chatto] = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        chatmessage=chatmessage.replace( "\r","")
        chatmessage=chatmessage.replace( "\n","<br>")

        if chatto not in  session['chatHistory']:
            session['chatHistory'][chatto]=[]

        session['chatHistory'][chatto].append({ 's': 1,'f':chatto,'m':chatmessage}); 

        if 'tsChatBoxes' in session:
            if chatto in session['tsChatBoxes']:
                del session['tsChatBoxes'][chatto]

        peer = Peer_Chat1(chatfrom,chatto,chatmessage,datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"),action=chataction)        
        
        db.session.add(peer)
        db.session.commit()
        
        #exit(0);

        self.response=jsonify(ok ="ok")
    


    def closeChat(self,request): 
        if 'openChatBoxes' in session:
            if request.args.get('chatbox') in session['openChatBoxes']:
                del session['openChatBoxes'][request.args.get('chatbox')]

        self.response=jsonify(ok ="ok")
    

    def startChatSession(self,request): 
        items=[]
        
        if 'openChatBoxes' in session:
            for chatbox,void1 in session['openChatBoxes'].items():
                items = items + self.chatBoxSession(chatbox)

        #items.append({ 's': 2,'f':"sri",'m':"hello"})
        #items.append({ 's': 2,'f':"sri1",'m':"hello1"})

        #self.response = jsonify(username=session['userid'],items=[items[:-1]])
        
        #ret = jsonify("{ username: "+session['userid']+", items: ["+items[:-1]+"]}")
        #self.response=flask.Response(response=ret, status=200, mimetype='application/json', content_type='application/json', direct_passthrough=False)

        mydata = {'username': session['userid'], 'items': items}
        self.response=Response(json.dumps(mydata,separators=(',',':')),  mimetype='application/json')

    def chatBoxSession(self,chatbox):     
            items=[] 
            if chatbox in session['chatHistory']:      
                items=session['chatHistory'][chatbox]
            return items
         
    def block(self,request): 
        username = request.args.get('username')
        uname = session['userid'];
        #echo "$uname has blocked nikhil $username";
        
        user = Blocked_Chat_Users.query.filter_by(Blocker=uname,Blocked=username).first()
        
        if user is None:
            user1 = Blocked_Chat_Users(0, uname, username,0)
            db.session.add(user1)
            #insert
        else:
            user.status=0
            #update
        db.session.commit()
        
        self.response=jsonify(ok ="ok")
    
    def webcam(self,request): 
        self.response=jsonify(ok ="ok")