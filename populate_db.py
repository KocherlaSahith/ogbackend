from database import Database
import hashlib

def populate_sample_data():
    db = Database()
    
    # Create sample users
    users = [
        ("admin", "admin@example.com", hashlib.md5("admin123".encode()).hexdigest()),
        ("john_doe", "john@example.com", hashlib.md5("john123".encode()).hexdigest()),
        ("jane_smith", "jane@example.com", hashlib.md5("jane123".encode()).hexdigest())
    ]
    
    user_ids = []
    for username, email, password_hash in users:
        try:
            user_id = db.create_user(username, email, password_hash)
            user_ids.append(user_id)
            print(f"Created user: {username}")
        except Exception as e:
            print(f"Error creating user {username}: {e}")
    
    # Create sample posts
    posts = [
        ("Welcome to our Website", "This is the first post on our amazing website!", user_ids[0]),
        ("Getting Started Guide", "Learn how to make the most of our platform.", user_ids[1]),
        ("Future Updates", "Exciting new features coming soon!", user_ids[2])
    ]
    
    for title, content, author_id in posts:
        post_id = db.create_post(title, content, author_id)
        print(f"Created post: {title}")
    
    # Create sample messages
    messages = [
        ("Alice Johnson", "alice@example.com", "Partnership Inquiry", "Hello, I'm interested in partnering with you."),
        ("Bob Wilson", "bob@example.com", "Technical Support", "I need help with my account."),
        ("Carol Davis", "carol@example.com", "Feedback", "Great website! Here are some suggestions...")
    ]
    
    for name, email, subject, message in messages:
        msg_id = db.create_message(name, email, subject, message)
        print(f"Created message from: {name}")
    
    print("Sample data population completed!")

if __name__ == "__main__":
    populate_sample_data()