from cafe_klatch import app
from flask import render_template,request,flash,session,url_for,redirect,jsonify
from forms import ContactForm, SignupForm, LoginForm, MatchesForm, ViewProfileForm, ChatForm,EditProfileForm,MessagesForm
from models import db,Peer_UserStatus_Model,User_Info_Model,Peer_Chat1, Blocked_Chat_Users
from sqlalchemy import update,or_,and_,create_engine
import operator
from werkzeug import secure_filename
from werkzeug.utils import secure_filename
import random
import smtplib
import os,traceback

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#@app.route('/mail/<verification_code>', methods =['GET','POST'])
def mail(verification_code):
    # me == my email address
    # you == recipient's email address
    me = "no.reply.cafe.klatch@gmail.com"
    you = session['email']

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Cafe Klatch Account Activation"
    msg['From'] = me
    msg['To'] = you
    

    url = "http://localhost:5000/activateProfile?user="+session['userid']+"&ver_code="+verification_code;
    print url
    # Create the body of the message (a plain-text and an HTML version).
    #text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = "<html><head><body>Hi "+ session['userid']+"<br/><br/>\
        Welcome to Cafe Klatch...!! Please click the below link to activate your account.<br/><br/>"+url+"\
        <br/>  <br/> <br/>   <br/>\
        <b>Note : If this link doesn't work, please paste it in your browser.</b><br/><br/> <br/>\
        Regards <br/>\
    Cafe Klatch Team\
    <br/>\
    <br/>\
    <img src='http://images.sussexpublishers.netdna-cdn.com/article-inline-half/blogs/55740/2011/06/65733-56133.jpg' alt='Cafe Klatch' height='100px' width='100px' />\
    </body></head></html>"
    print html
    # Record the MIME types of both parts - text/plain and text/html.
    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    #msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    try:
      s = smtplib.SMTP('smtp.gmail.com',587)
      s.ehlo()
      s.starttls()
      s.login('no.reply.cafe.klatch@gmail.com','Helloworld1')
      # sendmail function takes 3 arguments: sender's address, recipient's address
      # and message to send - here it is sent as one string.
      s.sendmail(me, you, msg.as_string())
      s.quit()
      return "Success"
    except Exception, er:
      return str(er)
      return "Failed"

@app.route('/activateProfile', methods =['GET','POST'])
def activateProfile():
   ver_code= request.args.get('ver_code')
   user= request.args.get('user')
   user = Peer_UserStatus_Model.query.filter_by(username=user,verfication_code=ver_code).first()
   user.isVerified=1
   db.session.commit()
   return render_template('activateProfile.html')   


@app.route('/signup', methods =['GET','POST'])
def signup():
    form = SignupForm() 
    
    #if 'userid' in session:
     #   return redirect(url_for('set_profile'))
    
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html',form = form)
        else:            
            verification_code = random.randint(1,10000)
            
            userlogin = Peer_UserStatus_Model(form.username.data, form.email.data, form.password.data,verification_code,0)            
            db.session.add(userlogin)
            db.session.commit()
            usersignup = User_Info_Model(form.username.data,'offline')
            db.session.add(usersignup)
            db.session.commit()
            session['userid'] = userlogin.username
            session['email'] = userlogin.email
            mail(str(verification_code))
            return render_template('verification_mail_confirmation.html')   
            
                    
    elif request.method == 'GET':
        return render_template('signup.html',form = form)   

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()  
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('index.html', form=form)
    else:
      session['userid'] = form.username.data     
      session['email'] = form.user.email 
      return redirect(url_for('view_profile'))
                 
  elif request.method == 'GET':
    return render_template('index.html', form=form)      

    
@app.route('/edit_profile', methods =['GET','POST'])
def edit_profile():  
    if 'userid' not in session:
        return redirect(url_for('login'))
    form = EditProfileForm()
    
    if request.form['hidden']=='view_profile':
        form.load_from_DB(request)
    elif request.form['button_hidden'] == 'save':
        form.saveAll_ExceptImage(request)
        return redirect(url_for('view_profile'))
    else:
        print "reached here"
        form.saveImage(request)
    print "also reached here"
    return render_template('set_profile.html',form = form)
    
@app.route('/chathistory')
def chathistory():
  if 'userid' not in session:
    return redirect(url_for('login'))
  username = session['userid']
  #user = db.session.query(Peer_Chat).filter(or_(Peer_Chat.From == username, Peer_Chat.To == username)).all()
  to = request.args.get("to")
  #print "________________________"
  #print to
  user = db.session.query(Peer_Chat1).from_statement("Select * from (Select * FROM peer_chat WHERE `from` = '"+to+ "' OR `to` = '"+to+ "') as T where `from` = '"+username+ "' OR `to` = '"+username+"'")

  return render_template('chat.html',user = user,username = username ) 
        
 
@app.route('/message')
def messages():
    if 'userid' not in session:
        return redirect(url_for('login'))
    
    form = MessagesForm()
    form.loadMessages()    
    return render_template("messages.html",form = form,messages = messages,result_fin = form.result_fin)



@app.route('/matches', methods=['GET', 'POST'])
def matches():
    if not 'userid' in session:
      return redirect(url_for('login'))
    form = MatchesForm()
    form.loadMatches()
    return render_template('matches.html', form=form) 
    
@app.route('/logout')
def logout():
    if 'userid' not in session:
        return redirect(url_for('login'))
    
    session.clear() 
    # for x in session: 
    #     session.pop(x, None)
    return redirect(url_for('login'))
    

@app.route('/view_profile')
def view_profile():
  if 'userid' not in session:
    return redirect(url_for('login'))
  form = ViewProfileForm()
  form.loadProfile()
  session['imagename']=form.user.imagename
  return render_template('view_profile.html', user=form.user)
    
@app.route('/chat/<action>')
def chat(action):
    if 'userid' not in session:
        return redirect(url_for('login'))
    form = ChatForm()
    
    if action == "chatheartbeat":
        form.chatHeartbeat(request) 
    elif action == "sendchat":
        form.sendChat(request) 
    elif action == "closechat":
        form.closeChat(request) 
    elif action == "startchatsession":
        form.startChatSession(request) 
    elif action == "block":
        form.block(request) 
    elif action == "webcam":
        form.webcam(request) 

    if 'chatHistory' not in session:
        session['chatHistory'] = {}

    if 'openChatBoxes' not in session:
        session['openChatBoxes']={}

    if 'tsChatBoxes' not in session:
        session['tsChatBoxes']={}

    return form.response

# @app.route('/_add_numbers')
# def add_numbers():
#     """Add two numbers server side, ridiculous but well..."""
#     a = request.args.get('a', 0, type=int)
#     b = request.args.get('b', 0, type=int)
#     return jsonify(result=a + b)

# @app.route('/ajax')
# def ajax():
#     return render_template('ajax.html')
    

@app.route('/sample') 
def sample():
    if 'userid' not in session:
      return redirect(url_for('login'))
    blocker = request.args.get('blocker')
    blocked = request.args.get('blocked')
    
    engine = create_engine('mysql://root:jasmeet@localhost/mysql')
    connection = engine.connect()
    result1 = connection.execute("Update blocked_chat_users set Status= 1 where Blocker ='" +blocker+ "' AND Blocked = '" +blocked+"'")

    return redirect(url_for('blocked'))
   

@app.route('/blocked')
def blocked():
    if 'userid' not in session:
      return redirect(url_for('login'))
    Blocker = session['userid']
    
    user_list = []
    sql_user = Blocked_Chat_Users.query.filter_by(Blocker= Blocker, Status= 0 ).all()
    print sql_user

    for sqluser in sql_user:
        userinfo = User_Info_Model.query.filter_by(userid=sqluser.Blocked).first()
        if not userinfo is None:
          user_list.append(userinfo)

    return render_template("blocked_chat.html", res_user = user_list)
