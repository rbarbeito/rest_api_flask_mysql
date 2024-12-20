from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQL_ALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

app.app_context().push()
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Modelo para acceder a la base de datos


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(40))

    def __init__(self, title, description):
        self.title = title
        self.description = description


# The `TaskSchema` class defines a schema with fields for task ID, title, and description.
class TaskSchema(ma.Schema):

    class Meta:
        fields = ("id", "title", "description")


db.create_all()

# `task_schema = TaskSchema()` creates an instance of the `TaskSchema` class, which is used to
# serialize a single task object into JSON format.
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


# Definimos las rutas en nuestra api rest


# create task
@app.route('/tasks', methods=['POST'])
def create_task():
    print(request.json)
    title = request.json["title"]
    description = request.json["description"]

    newTask = Task(title, description)
    db.session.add(newTask)
    db.session.commit()

    print('Almacenado correctamente en la base de datos')
    return task_schema.jsonify(newTask)

# get all task


@app.route('/tasks', methods=['GET'])
def get_all_task():
    all_task = Task.query.all()
    result = tasks_schema.dump(all_task)
    return jsonify(result)


@app.route('/task/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)


# Ruta de update
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):

    task = Task.query. session.get(Task, id)

    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    db.session.commit()

    return task_schema.jsonify(task)


@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.session.get(Task, id)
    db.session.delete(task)
    db.session.commit()

    return tasks_schema.jsonify(task)


@app.route('/tasks/delete', methods=['DELETE'])
def delete_all_task():
    db.session.query(Task).delete()
    db.commit()

    return jsonify({"message": "All task delete!!!"})


@app.route('/', methods=['GET'])
def index():
    return jsonify({"Message": "Welcome to my firts API Rest with Pyhton Flask"})


if __name__ == '__main__':
    app.run(debug=True)
