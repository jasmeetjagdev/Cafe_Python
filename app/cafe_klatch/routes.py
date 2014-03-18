from cafe_klatch import app
from flask import render_template,request,flash,session,url_for,redirect
from forms import ContactForm, SignupForm, SigninForm
from models import db,User


@app.route('/contact', methods = ['GET','POST'])
def contact():
    form1 = ContactForm()
    
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html',form = form)
        else:
            return 'Form posted.'    
    elif request.method == 'GET':
        return render_template('contact.html',form = form)  


@app.route('/signup', methods =['GET','POST'])
def signup():
    form = SignupForm() 
    
    if 'email' in session:
        return redirect(url_for('set_profile'))
    
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html',form = form)
        else:            
            newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            
            session['email'] = newuser.email
            return redirect(url_for('set_profile'))
                    
    elif request.method == 'GET':
        return render_template('signup.html',form = form)   
        

        
@app.route('/set_profile')
def set_profile():
    if 'email' not in session:
        return redirect(url_for('signin'))
     
    user = User.query.filter_by(email = session['email']).first()
 
    if user is None:
        return redirect(url_for('signin'))##
    else:
        return render_template('matches.html')     ##
        
@app.route('/')
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()  
  if 'email' in session:
      return redirect(url_for('set_profile'))
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('index.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('set_profile'))
                 
  elif request.method == 'GET':
    return render_template('index.html', form=form)      
    
@app.route('/signout')
def signout():
    if 'email' not in session:
        return redirect(url_for('signin'))
     
    session.pop('email', None)
    return redirect(url_for('signin'))
    
@app.route('/demo', methods=['GET', 'POST'])
def demo():
  form = Demo()
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('demo.html', form=form)
    else:
        newdemo = Demo(form.firstname.data, form.lastname.data)
        db.session.add(newdemo)
        db.session.commit()
      
  elif request.method == 'GET':
    return render_template('demo.html', form=form)
    
    
    
    
               