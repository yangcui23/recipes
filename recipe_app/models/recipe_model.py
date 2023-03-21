from recipe_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from recipe_app import DATABASE
from recipe_app.models import user_model


class Recipe:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.prepare_time = data['prepare_time']
        self.instruction = data['instruction']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create_recipe(cls, form):

        data = {
            **form,
            'user_id': session['user_id']
        }

        query = """ 
                INSERT INTO recipes (name , description , prepare_time, instruction ,created_at,user_id)
                VALUES (%(name)s,%(description)s,%(prepare_time)s,%(instruction)s,%(created_at)s,%(user_id)s)
                """

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one(cls, id):

        data = {
            'id': id
        }

        query = " SELECT * FROM recipes WHERE id = %(id)s"

        results = connectToMySQL(DATABASE).query_db(query, data)

        result = results[0]

        recipes = cls(result)

        return recipes
    
    @classmethod
    def get_one_with_user(cls,id):

        data = {
            "id" : id
        }
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"

        results = connectToMySQL(DATABASE).query_db(query,data)
        result = results[0]
        if results:
        
            recipe = cls(result)
            user_data = {
                **result,
                'id': result['users.id'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at'],
            }

            recipe.user = user_model.User(user_data)


        return recipe

    @classmethod
    def get_all(cls):

        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id"

        results = connectToMySQL(DATABASE).query_db(query)

        recipes = []

        if results:
            for row in results:
                recipe = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                }

                recipe.user = user_model.User(user_data)

                recipes.append(recipe)

        return recipes

    @staticmethod
    def validate_recipe(form):
        is_valid = True

        if len(form['name']) < 3 or len(form['name']) == 0:
            is_valid = False
            flash('First Name is too short!!!!!!')

        if len(form['description']) < 3:
            is_valid = False
            flash('Description is too short!!!!!!')

        if len(form['instruction']) < 3:
            is_valid = False
            flash('Instruction must be at least 3 characters!!!')
        

        return is_valid

    @classmethod
    def edit(cls, form, id):

        data = {
            **form,
            "id": id

        }
        query = """
                UPDATE recipes SET 
                name = %(name)s,
                instruction = %(instruction)s,
                description = %(description)s,
                prepare_time = %(prepare_time)s,
                created_at = %(created_at)s

                WHERE id = %(id)s
            """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s;"
        data = {"id": id}
        return connectToMySQL(DATABASE).query_db(query, data)
