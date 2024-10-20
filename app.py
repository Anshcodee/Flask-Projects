from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#Initialising database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #This is for SQLite, not MySQL 
db = SQLAlchemy(app)

#Creating a model:
class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self): # This is going to retrun the ID of a task, whenever a new task is created
    return '<Task %r>' %self.id # %r denotes the ID of the task


@app.route('/', methods=['POST','GET']) #index route(so that it doesn;t just give error 404 when browsing through the URL):
def index():    #defining a function for the route
  
  if request.method == 'POST':  #This specifies what will happen if we submit(POST) the form
    #Below is the logic for adding a task
    task_content = request.form['content'] #We'll pass the ID for the input we wanna get the contents of
    #Basically, task_content is the contents of wtv input is made
    new_task = Todo(content=task_content)

    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an issue adding your task'
  
  
  else:
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html',tasks=tasks)
  
@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
  task_to_delete = Todo.query.get_or_404(id) #If attempt to get ID fails, we'll get 404

  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  
  except:
    return "There was an error in deleting that task."

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
  task = Todo.query.get_or_404(id)
  if request.method == 'POST':
    #Below is the logic which changes the task's content to the one put in the update page
    task.content = request.form['content'] 

    try:
      db.session.commit()
      return redirect('/')
    except:
      return "There was an error in updating the task."
  
  else:
    return render_template('update.html', task=task)
  

# Add this block to create the database tables
#with app.app_context():
    # Below line creates the database, you only need to run the code.
    #db.create_all() # Comment this out after running and creating ONCE. 


if __name__ == "__main__":
  app.run(debug=True)

