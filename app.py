from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from database import Database

app = Flask(__name__)
CORS(app)
db = Database()

# Helper function to convert rows to dictionaries
def row_to_dict(row, columns):
    return {columns[i]: row[i] for i in range(len(columns))}

@app.route("/")
def home():
    return "Hello, Vercel!"

@app.route("/api")
def api():
    return "Hello, API!"

@app.route("/turtle")
def api2():
    return "Hello, Turtle!"

# Database API Routes
@app.route("/api/users", methods=['GET'])
def get_users():
    users = db.get_all_users()
    return jsonify(users)

@app.route("/api/users", methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = db.create_user(
        data['username'],
        data['email'],
        data['password_hash']  # In production, hash the password!
    )
    return jsonify({"message": "User created", "user_id": user_id})

@app.route("/api/posts", methods=['GET'])
def get_posts():
    posts = db.get_all_posts()
    columns = ['id', 'title', 'content', 'author_id', 'created_at', 'updated_at', 'is_published', 'username']
    posts_dict = [row_to_dict(post, columns) for post in posts]
    return jsonify(posts_dict)

@app.route("/api/posts", methods=['POST'])
def create_post():
    data = request.get_json()
    post_id = db.create_post(
        data['title'],
        data['content'],
        data['author_id']
    )
    return jsonify({"message": "Post created", "post_id": post_id})

@app.route("/api/messages", methods=['GET'])
def get_messages():
    messages = db.get_all_messages()
    columns = ['id', 'name', 'email', 'subject', 'message', 'created_at', 'is_read']
    messages_dict = [row_to_dict(msg, columns) for msg in messages]
    return jsonify(messages_dict)

@app.route("/api/messages", methods=['POST'])
def create_message():
    data = request.get_json()
    message_id = db.create_message(
        data['name'],
        data['email'],
        data.get('subject', ''),
        data['message']
    )
    return jsonify({"message": "Message sent", "message_id": message_id})

@app.route("/api/stats")
def get_stats():
    total_posts = len(db.get_all_posts())
    total_messages = len(db.get_all_messages())
    unread_messages = db.get_unread_messages_count()
    
    return jsonify({
        "total_posts": total_posts,
        "total_messages": total_messages,
        "unread_messages": unread_messages
    })

# Add this method to Database class if needed
def get_all_users(self):
    with self.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, created_at FROM users')
        return cursor.fetchall()

# Add this to the Database class
Database.get_all_users = get_all_users

if __name__ == "__main__":
    app.run()