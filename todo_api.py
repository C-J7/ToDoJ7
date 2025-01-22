from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

todos = [
    {"id": 1, "title": "Learn Python", "completed": False},
    {"id": 2, "title": "Build Todo App", "completed": False}
]
current_id = 3

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def create_todo():
    global current_id
    if not request.json or 'title' not in request.json:
        abort(400)
    
    todo = {
        'id': current_id,
        'title': request.json['title'],
        'completed': False
    }
    current_id += 1
    todos.append(todo)
    return jsonify(todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        abort(404)
    
    data = request.get_json()
    todo['title'] = data.get('title', todo['title'])
    todo['completed'] = data.get('completed', todo['completed'])
    return jsonify(todo)

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        abort(404)
    
    todos = [t for t in todos if t['id'] != todo_id]
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)