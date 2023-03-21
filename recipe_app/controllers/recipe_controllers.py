from recipe_app import app
from flask import render_template , request , redirect ,session ,flash

from recipe_app.models.user_model import User
from recipe_app.models.recipe_model import Recipe


@app.route('/recipe')
def recipe():
    if 'user_id' not in session:
        flash('Please Login to proceed the page')
        return redirect('/')
    user = User.get_one(session['user_id'])
    recipes = Recipe.get_all()
    
    return render_template('recipe.html', user=user,recipes=recipes)


@app.route('/recipe/new')
def new_recipe():
    if 'user_id' not in session:
        flash('Please Login to proceed the page')
        return redirect('/')
    return render_template('new_re.html')



@app.route('/recipe/new_recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        flash('Please Login to proceed the page')
        return redirect('/')
    print(request.form)
    if not Recipe.validate_recipe(request.form):

        return redirect("/recipe/new")
    Recipe.create_recipe(request.form)
    return redirect('/recipe')

@app.route('/recipe/view/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        flash('Please Login to proceed the page')
        return redirect('/')
    user = User.get_one(session['user_id'])
    recipes = Recipe.get_one_with_user(id)
    

    return render_template('dish.html' ,recipe=recipes,user=user,)

@app.route('/recipe/edit/<int:id>')
def update_recipe(id):
    if 'user_id' not in session:
        flash('Please Login to proceed the page')
        return redirect('/')
    
    recipe = Recipe.get_one(id)
    return render_template('edit_re.html',recipe=recipe)



@app.route('/recipe/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        flash('Please Login to proceed the page')
        return redirect('/')
    Recipe.delete(id)
    return redirect('/recipe')


@app.route('/edit/<int:id>',methods=['POST'])
def edit(id):
    if 'user_id' not in session:
        flash('Please Login to proceed the page')
        return redirect('/')
    if not Recipe.validate_recipe(request.form):

        return redirect(f"/recipe/edit/{id}")
    Recipe.edit(request.form,id)
    return redirect('/recipe')