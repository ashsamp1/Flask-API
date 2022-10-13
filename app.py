from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

#Creating Models for Databases.

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post ' + str(self.id)

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

all_posts = [
    {
        'title' : 'Post 1 ',
        'content' : ' This is content of post 1',
        'author' : 'Akash'
    },
    {
        'title' : 'Post 2 ',
        'content' : ' This is content of post 2'
    }
]

@app.route("/posts",methods=['GET','POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author='Akash')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()

    return render_template('posts.html',posts=all_posts)

@app.route('/home/<int:id>')
def hello(id):
    return "Hello, "+str(id)

@app.route('/onlyget',methods=['GET'])
def get_req():
    return "You can only get this"

#Adding dib by 0 using decorator
def smart_divide(func):
    def inner(a,b):
        print("I am going to divide",a,"and",b)
        if b == 0:
            print("Whoops! cannot divide")
            return
        return func(a,b)
    return inner

@smart_divide
def divide(a,b):
    return a/b


@app.route('/divide', methods = ['GET','POST'])
def divide_numbers():
    if request.method == 'POST':
        body = request.json
        num1 = body['num1']
        num2 = body['num2']

        res = divide(int(num1),int(num2))

        return jsonify({'result = ' : res})


if __name__ == "__main__":
    app.run(debug=True)
