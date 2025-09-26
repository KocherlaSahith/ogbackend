import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_path='website.db'):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        with self.get_connection() as conn:
            # Users table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Posts table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    author_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_published BOOLEAN DEFAULT 0,
                    FOREIGN KEY (author_id) REFERENCES users (id)
                )
            ''')
            
            # Messages table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    subject TEXT,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_read BOOLEAN DEFAULT 0
                )
            ''')
            
            conn.commit()
    
    # User methods
    def create_user(self, username, email, password_hash):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))
            conn.commit()
            return cursor.lastrowid
    
    def get_user_by_id(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            return cursor.fetchone()
    
    def get_user_by_username(self, username):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            return cursor.fetchone()
    
    # Post methods
    def create_post(self, title, content, author_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO posts (title, content, author_id, is_published)
                VALUES (?, ?, ?, ?)
            ''', (title, content, author_id, True))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_posts(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, u.username 
                FROM posts p 
                JOIN users u ON p.author_id = u.id 
                WHERE p.is_published = 1 
                ORDER BY p.created_at DESC
            ''')
            return cursor.fetchall()
    
    def get_post_by_id(self, post_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, u.username 
                FROM posts p 
                JOIN users u ON p.author_id = u.id 
                WHERE p.id = ?
            ''', (post_id,))
            return cursor.fetchone()
    
    # Message methods
    def create_message(self, name, email, subject, message):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO messages (name, email, subject, message)
                VALUES (?, ?, ?, ?)
            ''', (name, email, subject, message))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_messages(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM messages ORDER BY created_at DESC')
            return cursor.fetchall()
    
    def get_unread_messages_count(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM messages WHERE is_read = 0')
            return cursor.fetchone()[0]