from recipe_app import app 

from recipe_app.controllers import  recipe_controllers , user_controllers

if __name__== '__main__':  
    app.run(debug=True) 