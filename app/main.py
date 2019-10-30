import os
import dialogflow

from clarifai.rest import ClarifaiApp

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from google.cloud import storage
from flask import jsonify
from werkzeug.utils import secure_filename

import speech_recognition as sr
import subprocess
from google.cloud import texttospeech
import os

from audio import Audio
from flask import send_file, send_from_directory, safe_join, abort


#NEW
UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
#----

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#NEW
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# how to not reset the values 
class DataStore: 
    HASAUDIO = False

#----
db = SQLAlchemy(app)
app.secret_key = "flash message"

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    time = db.Column(db.Integer, nullable=False)
    serving = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)
    Cooks = db.relationship('Cook', backref='recipe', lazy=True)

    def __repr__(self):
        return '<Recipe %r>' % self.id


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __repr__(self):
        return '<Ingredient %r>' % self.id


class Cook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    step = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __repr__(self):
        return '<Cook %r>' % self.id


@app.route('/')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)


@app.route('/bot', methods=['POST', 'GET'])
def bot():
	return render_template('bot.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    return render_template('add.html')

@app.route('/add_image', methods=['POST', 'GET'])
def add_image():
    return render_template('image-add.html')


@app.route('/food/<int:id>', methods=['POST', 'GET'])
def food(id):
    recipes = Recipe.query.filter_by(id=id).first()
    ingredients = Ingredient.query.filter_by(recipe_id=id)
    cooks = Cook.query.filter_by(recipe_id=id)
    return render_template('food.html', recipes=recipes, cooks=cooks, ingredients=ingredients)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        recipe_name = request.form['recipe[name]']
        recipe_time = request.form['recipe[time]']
        recipe_serving = request.form['recipe[serving]']
        recipe_description = request.form['recipe[description]']
        recipe_image = request.files['recipe[pic]']
        ingredient_name = request.form['ingredient-name[0]']
        ingredient_quantity = request.form['ingredient-quantity[0]']
        cook_name = request.form['cook-name[0]']
        cook_step = request.form['cook-step[0]']

        recipe_image_url = upload_blob('recipes-pic', recipe_image, (recipe_name + '.jpg').replace(" ", ""))

        new_recipe = Recipe(name=recipe_name, time=recipe_time, serving=recipe_serving, description=recipe_description, image_file=recipe_image_url)
        try:
            db.session.add(new_recipe)
            db.session.commit()

            user_return = Recipe.query.filter_by(name=recipe_name).first()

            new_ingredient = Ingredient(name=ingredient_name, quantity=ingredient_quantity, recipe_id=user_return.id)
            db.session.add(new_ingredient)

            new_cook = Cook(name=cook_name, step=cook_step, recipe_id=user_return.id)
            db.session.add(new_cook)

            db.session.commit()

            flash('Data Inserted Successfully.', 'success')
            return redirect(url_for('index', scroll='anchor'))
        except:
            flash('Data Inserted Unsuccessfully.', 'danger')
            return redirect(url_for('index', scroll='anchor'))


@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    try:
        Cook.query.filter(Cook.recipe_id == id).delete()
        Ingredient.query.filter(Ingredient.recipe_id == id).delete()
        Recipe.query.filter(Recipe.id == id).delete()
        db.session.commit()
        flash('Data Deleted Successfully.', 'success')
        return redirect(url_for('index', scroll='anchor'))
    except:
        flash('Data Deleted Unsuccessfully.', 'danger')
        return redirect(url_for('index', scroll='anchor'))


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    recipes = Recipe.query.filter_by(id=id).first()
    ingredients = Ingredient.query.filter_by(recipe_id=id)
    cooks = Cook.query.filter_by(recipe_id=id)
    if request.method == 'POST':
        recipes.name = request.form['recipe[name]']
        recipes.time = request.form['recipe[time]']
        recipes.serving = request.form['recipe[serving]']
        recipes.description = request.form['recipe[description]']
        ingredients.name = request.form['ingredient-name[0]']
        ingredients.quantity = request.form['ingredient-quantity[0]']
        cooks.name = request.form['cook-name[0]']
        cooks.step = request.form['cook-step[0]']
        try:
            db.session.commit()
            flash('Data Edited Successfully.', 'success')
            return redirect(url_for('index', scroll='anchor'))
        except:
            flash('Data Inserted Unsuccessfully.', 'danger')
            return redirect(url_for('index', scroll='anchor'))
    else:
        return render_template('update.html', recipes=recipes, cooks=cooks, ingredients=ingredients)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

cfapp = ClarifaiApp(api_key="14e719029ce04f1ea05d1c6d01d05d56")

def getPrediction():
    model = cfapp.models.get('food-items-v1.0')
    response = model.predict_by_bytes('/home/user/image.jpeg')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print("in upload")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            
            filename = secure_filename(file.filename)

            model = cfapp.models.get('food-items-v1.0')
            response = model.predict_by_bytes(file.read())

            print(response)
            concepts = response['outputs'][0]['data']['concepts']
            topConcepts = []
            file.seek(0) # to reset file reader to the start

            for concept in concepts:
                print(concept['name'], concept['value'])
                if concept['value'] >= 0.5:
                     topConcepts.append(concept)

            ing_recipe_url = upload_blob('ingredient-pics', file, (file.filename + '.jpg').replace(" ", ""))
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file',filename=filename))
            return render_template('image-add.html', submission_successful=True, concepts=topConcepts, file_url=ing_recipe_url)
           

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client(project="smart-recipes-cc")
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(source_file_name)
    return blob.public_url

@app.route('/insert-image', methods=['POST'])
def insert_image():
    if request.method == "POST":
        recipe_name = request.form['recipe[name]']
        recipe_time = request.form['recipe[time]']
        recipe_serving = request.form['recipe[serving]']
        recipe_description = request.form['recipe[description]']
        recipe_image = request.files['recipe[pic]']
        # ingredient_name = request.form['ingredient-name[0]']
        # ingredient_quantity = request.form['ingredient-quantity[0]']
        # cook_name = request.form['cook-name[0]']
        # cook_step = request.form['cook-step[0]']

        checkedIngredients = request.form.getlist("ingCheckbox")
        ingredientQty = request.form.getlist("ingCheckboxAmt")
        addedIngredients = request.form.getlist("newIng")
        addedIngredientsQty = request.form.getlist("newIngQty")

        steps = request.form.getlist("stepName")

        #add all the ingredients together to create one ingredents array 
        nameIndex = 0
        ingredientsArray = []
        for qty in ingredientQty:
            if qty != '':
                ingredientElement = {
                    'qty' : qty,
                    'name': checkedIngredients[nameIndex]
                }
                ingredientsArray.append(ingredientElement)
                nameIndex = nameIndex+1
        
        for i, name in enumerate(addedIngredients):
            ingredientElement = {
                    'qty' : addedIngredientsQty[i],
                    'name': name
                }
            ingredientsArray.append(ingredientElement)
            

        recipe_image_url = upload_blob('recipes-pic', recipe_image, (recipe_name + '.jpg').replace(" ", ""))

        new_recipe = Recipe(name=recipe_name, time=recipe_time, serving=recipe_serving, description=recipe_description, image_file=recipe_image_url)
        try:
            db.session.add(new_recipe)
            db.session.commit()

            user_return = Recipe.query.filter_by(name=recipe_name).first()

            #then put this in a loop for each element of the ing array
            for ing in ingredientsArray:
                new_ingredient = Ingredient(name=ing['name'], quantity=ing['qty'], recipe_id=user_return.id)
                db.session.add(new_ingredient)

            # will have to do the same with step
            for i, step in enumerate(steps):
                new_cook = Cook(name=step, step=i+1, recipe_id=user_return.id)
                db.session.add(new_cook)

            db.session.commit()

            flash('Data Inserted Successfully.', 'success')
            return redirect(url_for('index', scroll='anchor'))
        except:
            flash('Data Inserted Unsuccessfully.', 'danger')
            return redirect(url_for('index', scroll='anchor'))




@app.route('/getAudioData', methods=['GET', 'POST'])
def getAudioData():
    if app.config['HASAUDIO'] == False: 
        try:
            return send_from_directory("./audio/ing/", filename="./audio/ing/" + app.config['RECIPENO'] + "/ings.zip", as_attachment=True)
        except FileNotFoundError:
            abort(404)
    
    else: 
        wait = {"audio": False}
        return jsonify(wait)

@app.route('/play-recipe/<int:id>', methods=['GET', 'POST'])
def playRecipe(id):
    # Get the recipe we want
    recipes = Recipe.query.filter_by(id=id).first()
    ingredients = Ingredient.query.filter_by(recipe_id=id)
    method = Cook.query.filter_by(recipe_id=id)

    audio = Audio()
    # Generate audio files for selected recipe
    pathI = "./audio/" + str(id) + "/ing/" 
    pathM = "./audio/" + str(id) + "/method/"
    path = "./audio/" + str(id) + "/"

    print(recipes)
    print(ingredients)
    print(method)
    jsonObj = {
        'recipeName': recipes.name
    }
    for i, ing in enumerate(ingredients):
        print(ing.name)
        strIndex = str(i)
        jsonObj['ing'] = {
            i: ing.name
        }
    return jsonify(jsonObj)
    # for ingredient in ingredients:
    #     fileToSave = pathI + ingredient.name
    #     ingString = ingredient.quantity + " " + ingredient.name

    #     audio.createAudioFiles(ingString, fileToSave)

    # for step in method:
    #     fileToSave = pathM + str(step.step)
    #     methodString = step.name

    #     audio.createAudioFiles(methodString, fileToSave)
   
    # if audio.createZip(path+"/recipe.zip") == True:
    #     try:
    #         safe_path = safe_join(path, "recipe.zip")
    #         return send_file(safe_path, as_attachment=True)
    #     except FileNotFoundError:
    #         abort(404)
    # else:
    #     return "false"


    
if __name__ == '__main__':
    app.run()
