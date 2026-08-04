from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required
from .models import Image

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("index.html")

@views.route('/about-us')
def about_us():
    return render_template("about-us.html")

@views.route('/401')
def page401():
    return render_template("401.html")

@views.route('/404')
def page404():
    return render_template("404.html")

@views.route('/access-denied')
def access_denied():
    return render_template("access-denied.html")

@views.route('/account-page')
def account_page():
    return render_template("account-page.html")

@views.route('/contact-us')
def contact_us():
    return render_template("contact-us.html")



@views.route('/game-categories')
def game_categories():
    return render_template("game-categories.html")

@views.route('/guide-page')
def guide_page():
    return render_template("guide-page.html")


@views.route('/manage-game')
def manage_game():
    return render_template("manage-game.html")


@views.route('/reset-password')
def reset_password():
    return render_template("reset-password.html")

@views.route('/t2i-page')
@login_required
def t2i_page():
    return render_template("t2i-page.html")

@views.route('/test')
def test():
    return render_template("test.html")

@views.route('/update-password')
def update_password():
    return render_template("update-password'.html")



# categories 
@views.route('/body-parts-category')
def body_parts():
    images = Image.query.filter_by(category='Body_part').all()
    return render_template("body-parts-category.html" ,images=images)

@views.route('/food-category')
def food():
    images = Image.query.filter_by(category='food').all()
    return render_template("food-category.html", images=images)

@views.route('/books-category')
def books():
    images = Image.query.filter_by(category='book').all()
    return render_template("books-category.html", images=images)

@views.route('/sports-category')
def sports():
    images = Image.query.filter_by(category='sport').all()
    return render_template("sports-category.html", images=images)

@views.route('/nature-category')
def nature():
    images = Image.query.filter_by(category='nature').all()
    return render_template("nature-category.html", images=images)


@views.route('/animals')
def animals():
    images = Image.query.filter_by(category='animal').all()
    return render_template("animals-category.html", images=images)

@views.route('/jobs')
def jobs():
    images = Image.query.filter_by(category='job').all()
    return render_template("jobs-category.html", images=images)

@views.route('/toys')
def toys():
    images = Image.query.filter_by(category='toy').all()
    return render_template("toys-category.html", images=images)

@views.route('/family')
def family():
    images = Image.query.filter_by(category='family').all()
    return render_template("family-category.html", images=images)

@views.route('/culture')
def culture():
    images = Image.query.filter_by(category='Culture').all()
    return render_template("culture-category.html", images=images)



@views.route('/<int:image_id>')
def image_details(image_id):
    image = Image.query.get_or_404(image_id)
    return render_template('specific-image-page.html', image=image)



