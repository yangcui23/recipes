from recipe_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from recipe_app import DATABASE , bcrypt
from recipe_app.models import recipe_model

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @classmethod
    def create(cls,form):

        
        hashed_pw = bcrypt.generate_password_hash(form['password'])
        data = {
            **form,
            'password' : hashed_pw
        }

        query = """
            INSERT INTO users(first_name,last_name,email,password) 
            VALUES (%(first_name)s ,%(last_name)s , %(email)s , %(password)s)

        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_one_email(cls,email):

        

        query = "SELECT * FROM users WHERE email = %(email)s;"

        results = connectToMySQL(DATABASE).query_db(query, email)

        if results:

            return cls(results[0])
        else :
            return False

    @classmethod
    def get_all(cls):

        query = "SELECT * FROM users"

        results = connectToMySQL(DATABASE).query_db(query)

        users = []

        if results:
            for row in results:
                new_user = cls(row)

                users.append(new_user)

        return users
    
    @classmethod
    def get_one(cls, id):

        data = {
            "id": id,
        }

        query = """
            SELECT * FROM users WHERE id = %(id)s
        """

        results = connectToMySQL(DATABASE).query_db(query,data)

        result = results[0]

        users = cls(result)

        return users

    # @classmethod
    # def get_one_with_recipes(cls,data):
    #     data = {
    #         'id' : id
    #     }

    #     query = "SELECT * FROM users JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(id)s;"
    
    #     results = connectToMySQL(DATABASE).query_db(query,data)
    #     recipes = []

    #     if results:
    #         user = cls(results[0])


    #         for row in results:

    #             recipes_data = {
    #                 **row,
    #                 'id' : row['recipes.id'],
    #                 'created_at' : row['recipes.created_at'],
    #                 'updated_at' : row['recipes.updated_at']

    #             }

    #             new_recipe = recipe_model.Recipe(recipes_data)

    #             recipes.append(new_recipe)

    #         user.recipes = recipes

    #     return recipes





    @classmethod
    def validate(cls,form):

        is_valid = True

        if len(form['first_name']) < 3 or len(form['first_name']) == 0 :
            is_valid = False
            flash('First Name is too short!!!!!!')
        
        if len(form['last_name']) < 3:
            is_valid = False
            flash('Last Name is too short!!!!!!')
        
        if not EMAIL_REGEX.match(form['email']):
            is_valid = False
            flash('Invalid Email format!!!!!!')

        if cls.get_one_email(form['email']):
            is_valid = False
            flash('Email has already been registered, please pick another!!!')

        if len(form['password']) < 8 :
            is_valid = False
            flash('Password must be at least 6 characters!!!')

        if form['password'] != form['confirm_password']:
            is_valid  = False
            flash('Password must match!!!')


        return is_valid

    @classmethod
    def validate_login(cls,form):

        found_user = cls.get_one_email(form)

        if found_user:
            if bcrypt.check_password_hash(found_user.password , form['password']):
                return found_user
            else:
                flash('Invalid Login')
                return False
            
        else:
            flash('Invalid Login')
            return False