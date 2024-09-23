import sentry_sdk 
from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Cấu hình cơ sở dữ liệu SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'your-secret-key'  # Secret key cho form và flash messages

# Initialize the app with SQLAlchemy
db = SQLAlchemy(app)

# Model Todo
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Route chính
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)
 
    

# Route với tham số
@app.route('/hello/<name>')
def hello_name(name):
    return f'Hello, {name}!'

# Trang home với danh sách post giả lập
@app.route('/home')
def home():
    user = {'nickname': 'Nong'}  # Dữ liệu giả lập
    posts = [  # Dữ liệu post giả lập
        {
            'author': {'nickname': 'lucy'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'thuy'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('home.html', title='Home', user=user, posts=posts)

#Sentry
sentry_sdk.init(
    dsn="http://fca8c9afaa0a53fc517b39405aa80ea6@172.21.21.10:9000/6",
    traces_sample_rate=1.0  # Chỉ định tỷ lệ mẫu cho việc theo dõi
)

#Sentry exception
@app.route("/flask-ops")
def hello_exception():
    1/0  # raises an error
    return "<p>Error 404!</p>"

@app.errorhandler(Exception)
def handle_exception(e):
    # Gửi lỗi đến Sentry
    sentry_sdk.capture_exception(e)
    return "An error occurred", 500

# Chạy ứng dụng
if __name__ == "__main__":
    app.run(host='172.21.21.12', port=5000, debug=True)
