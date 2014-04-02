from cafe_klatch import app
from flask import render_template,request,flash,session,url_for,redirect,jsonify
from forms import ContactForm, SignupForm, LoginForm, MatchesForm, ViewProfileForm, ChatForm,EditProfileForm,MessagesForm
from models import db,Peer_UserStatus_Model,User_Info_Model,Peer_Chat1
from sqlalchemy import update,or_,and_,create_engine
import operator
from werkzeug import secure_filename
from werkzeug.utils import secure_filename
import random


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
            
            userlogin = Peer_UserStatus_Model(form.username.data, form.email.data, form.password.data,verification_code,1)            
            db.session.add(userlogin)
            db.session.commit()
            usersignup = User_Info_Model(form.username.data,'offline')
            db.session.add(usersignup)
            db.session.commit()
            
            session['userid'] = userlogin.username
            session['email'] = userlogin.email
            return redirect(url_for('view_profile'))
                    
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
    
#                