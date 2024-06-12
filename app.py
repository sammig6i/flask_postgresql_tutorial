from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flaskuser:flaskpassword@localhost:5432/flaskappdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(50), unique=True, nullable=False)

  def __repr__(self):
    return f'<User {self.name}>'
  
@app.route('/')
def index():
  return "Hello World!"

@app.route('/users', methods=['POST'])
def add_user():
  data = request.get_json()
  new_user = User(name=data['name'], email=data['email'])
  db.session.add(new_user)
  db.session.commit()
  return jsonify({"message": "User added"}), 201

@app.route('/users', methods=['GET'])
def get_users():
  users = User.query.all()
  return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
  user = User.query.get_or_404(id)
  return jsonify({'id': user.id, 'name': user.name, 'email': user.email})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
  data = request.get_json()
  user = User.query.get_or_404(id)
  user.name = data['name']
  user.email = data['email']
  db.session.commit()
  return jsonify({"message": "User updated"})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
  user = User.query.get_or_404(id)
  db.session.delete(user)
  db.session.commit()
  return jsonify({"message": "User deleted"})






