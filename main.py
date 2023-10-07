# Written by Alexander Dave Flores Respicio
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Create Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tasks.db"
# Create the extension
db = SQLAlchemy()
# initialise the app with the extension
db.init_app(app)


# Create Table
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(500), unique=True, nullable=False)

# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    # Read all records
    # Construct a query to select from the database. Returns the rows in the database
    result = db.session.execute(db.select(Task).order_by(Task.task))
    # Use .scalars() to get the elements rather than entire rows from the database
    all_tasks = result.scalars()
    return render_template("index.html", tasks=all_tasks)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # Create record
        new_task = Task(
            task=request.form["task"]
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("index.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # Update Record
        task_id = request.form["id"]
        task_to_update = db.get_or_404(Task, task_id)
        task_to_update.task = request.form["task"]
        db.session.commit()
        return redirect(url_for('home'))
    task_id = request.args.get('id')
    task_selected = db.get_or_404(Task, task_id)
    return render_template("edit.html", task=task_selected)


@app.route("/delete")
def delete():
    task_id = request.args.get('id')
    # Delete a record by id
    task_to_delete = db.get_or_404(Task, task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
