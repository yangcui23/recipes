from recipe_app import app
from flask import render_template , request , redirect ,session ,flash

from recipe_app.models.user_model import User


@app.route('/')
def index():
    
    return render_template('register.html')


@app.route('/create_user',methods=['POST'])
def create():

    
    if not User.validate(request.form):

        return redirect('/')
    
    # User.create(request.form)
    session['user_id'] = User.create(request.form)
    
    return redirect('/recipe')



@app.route('/login_user',methods=['POST'])
def login():

    login_in = User.validate_login(request.form)


    if login_in:
        user = User.get_one_email(request.form)
        session['user_id'] = user.id
        return redirect('/recipe')
        
    else:
        return redirect('/') 
    




@app.route('/logout')
def logout():

    session.clear()
    return redirect('/')