from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, current_app, request
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Top Secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#  Define a database and pass our app to the SQLAlchemy
db = SQLAlchemy(app)

app.app_context().push()



# with app.app_context():
#     # within this block, current_app points to app.
#     print(current_app.name)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), nullable=False, default='pic.jpg')
    email = db.Column(db.String(200), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    # To create a user on its own
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Helps in creation of the object
    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"


posts = [
    {
        'author': 'Nirmal Adhikari',
        'title': 'First Post',
        'content': 'Hustle for Moru Internship Grant',
        'date_posted': 'April 01, 2023',
    },
    {
        'author': 'Bimal Magar',
        'title': 'Second Post',
        'content': 'Happy New Year',
        'date_posted': 'January 01, 2023',
    },
    {
        'author': 'Bibek Pandey',
        'title': 'Third Post',
        'content': 'I am not sure about anything.',
        'date_posted': 'Feb 01, 2023',
    },
]



@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html', posts=posts)



@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created! Username: {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Credentials do not match', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route('/add')
def add():
    return render_template('addpost.html')



@app.route('/addpost', methods=['POST', 'GET'])
def addpost():
    return f"title: {request.form['title']} content: {request.form['content']}"
# Create a database

db.create_all()
db.drop_all()
db.create_all()


# user1 = User(username='Nirmal', email='nirmal@gmail.com', password='helloWorld')
# user2 = User(username='Bimal', email='bimal@gmail.com', password='bimal')
# user3 = User(username='Bibek', email='bibek@gmail.com', password='bibek')
# db.session.add(user1)
# db.session.add(user2)
# db.session.add(user3)
# db.session.commit()

# post1 = Post(title='PostNirmal', content="Nirmal's first post.", user_id=user1.id)
# post2 = Post(title='PostBimal', content="Bimal's first post.", user_id=user2.id)
# post3 = Post(title='PostBibek', content="Bibek's first post.", user_id=user3.id)
# db.session.add(post1)
# db.session.add(post2)
# db.session.add(post3)
# db.session.commit()


# Let's create our main class
if __name__ == '__main__':
    app.run(debug=True)




