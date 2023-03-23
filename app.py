from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# db.init_app(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=False)



@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# add task
@app.route('/add', methods=['POST'])
def add():
    task_name = request.form['task_name']
    new_task = Task(task_name=task_name)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('home'))

# update task
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    task = Task.query.get_or_404(id)
    task.status = not task.status
    db.session.commit()
    return redirect(url_for('home'))

# delete task
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
   with app.app_context():
    db.create_all()
    app.run(debug=True,port=8000)