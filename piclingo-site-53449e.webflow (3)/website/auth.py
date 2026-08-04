from flask import Blueprint, render_template, flash, redirect, url_for, request 
from flask_login import current_user, login_required, login_user, logout_user

from .models import Mentor , Image , Favorite
from . import db   ##means from __init__.py import db
import base64
import os
from werkzeug.utils import secure_filename
import uuid


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Mentor.query.filter_by(email=email).first()
        if user:
            if (user.password == password):
                login_user(user)
                print("sucess!!")
                return redirect(url_for('auth.account'))
            else:
                print("wrong password")
                flash('Incorrect password, try again.', category='error')
        else:
            print("email not exist")
            flash('email does not exist', category='error')

    return render_template("log-in.html")

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = Mentor.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Mentor(fullName=name , email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            print("sucess!!")
            return redirect(url_for('auth.account'))


    return render_template("sign-up.html")


@auth.route('/account')
@login_required
def account():
    if current_user.is_authenticated:
        user_name = current_user.fullName
    else:
        user_name = ""  
    return render_template("mentor.html", user_name = user_name )




#--------------------Save image and caption from model into database---------------------
@auth.route('/save-image', methods=['POST','GET'])
def save_image():
    caption = request.form.get('caption')
    image = request.files['image']
    category = request.form.get('category')

    if not image or not caption:
        return 'No image or caption provided', 400

    # Ensure the 'generated_images' folder exists under the 'static' folder
    UPLOAD_FOLDER = os.path.join('website', 'static', 'generated_images')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Generate a unique filename for the image
    filename = str(uuid.uuid4()) + '.png'
    image_path = os.path.join(UPLOAD_FOLDER, filename)

    # Save the image to the 'generated_images' folder
    image.save(image_path)

    # Generate the URL for the saved image
    image_url = url_for('static', filename=os.path.join('generated_images', filename))

    # Now, save the image URL in the database
    new_image = Image(image=image_url, 
                    category=category, 
                    caption=caption)
    db.session.add(new_image)
    db.session.commit()

    # Pass the image ID to the 'add_favorite' route
    return redirect(url_for('auth.add_favorite', image_id=new_image.id))


@auth.route('/add_favorite', methods=['POST', 'GET'])
def add_favorite():
    if current_user.is_authenticated:  
       image_id = request.args.get('image_id')  # Retrieve the image ID from the query parameters

       if image_id:
            favorite = Favorite(mentor_id=current_user.id, image_id=image_id)
            db.session.add(favorite)
            db.session.commit()
    
       else:
            flash('No image ID provided', category='error')
    else:
        flash('You need to log-in first', category='error')

    return render_template("t2i-page.html")

#--------------------manage the content of image categories (Upload image with caption, Delete image)----------------
@auth.route('/upload_image', methods=['POST','GET'])
def upload_image():
    if request.method == 'POST':
        category = request.form.get('category')
        image = request.files['image']
        caption = request.form.get('captionImage')

    if not image or not category:
        flash('no image or category provided', 'error')
        return render_template('manage-game.html')
    
    # Ensure the 'generated_images' folder exists under the 'static' folder
    UPLOAD_FOLDER = os.path.join('website', 'static', 'generated_images')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Generate a unique filename for the image
    filename = str(uuid.uuid4()) + '.png'
    image_path = os.path.join(UPLOAD_FOLDER, filename)

    # Save the image to the 'generated_images' folder
    image.save(image_path)

    # Generate the URL for the saved image
    image_url = url_for('static', filename=os.path.join('generated_images', filename))

    new_image = Image(image= image_url, 
                      category= category, 
                      caption= caption, 
                      )  
      
    db.session.add(new_image)
    db.session.commit()

    flash('Image uploaded successfully', 'success')
    return render_template('manage-game.html')

#----------------------------------------------------------------------
@auth.route('/display_images', methods=['POST','GET'])
def display_images():
    if request.method == 'POST':
        category = request.form.get('category')
        images = Image.query.filter_by(category=category).all()
        if not images:
            flash('No images found for the selected category', 'warning')
    else:
        images = []

    return render_template('manage-game.html', images=images)

#----------------------------------------------------------------------

@auth.route('/delete-image/<int:image_id>', methods=['GET','POST'])
def delete_image(image_id):
    #favorite_image = Favorite.query.filter_by(image_id=image_id).first()
    image = Image.query.get(image_id)
    if image:
        db.session.delete(image)
        db.session.commit()
        flash('Image deleted successfully', 'success')
        return render_template('manage-game.html')
    else:
        flash('Image not found', 'error')
        return render_template('manage-game.html')
    

#----------------------------------------------------------------------

@auth.route('/favorite-list')
@login_required
def favorite_list():
    # Query the database for the user's favorite images
    favorite_images = db.session.query(Image).join(Favorite).filter(Favorite.mentor_id == current_user.id).all()
    return render_template('favorite-list.html', favorite_images=favorite_images)


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))  # Redirect to the login page after logout

