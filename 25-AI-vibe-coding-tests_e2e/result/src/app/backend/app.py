"""
Simple Web Blog Application - Backend
Flask REST API with MySQL database
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Database Configuration
# Set USE_SQLITE=true to use SQLite instead of MySQL (easier for development)
USE_SQLITE = os.environ.get('USE_SQLITE', 'true').lower() == 'true'

if USE_SQLITE:
    # SQLite configuration (default for easy development)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, 'blog.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    print(f"Using SQLite database: {DB_PATH}")
else:
    # MySQL configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'blog_db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    print(f"Using MySQL database: {DB_NAME}")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ============================================================================
# Database Models
# ============================================================================

class User(db.Model):
    """User model for blog authors"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with posts
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'post_count': len(self.posts)
        }


class Post(db.Model):
    """Post model for blog posts"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_id': self.user_id,
            'author': self.author.username if self.author else None
        }


# ============================================================================
# API Routes - Users
# ============================================================================

@app.route('/api/users', methods=['GET'])
def get_users():
    """List all users"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details by ID"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({'error': 'Username and email are required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email']
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user by ID"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User {user_id} deleted successfully'})


# ============================================================================
# API Routes - Posts
# ============================================================================

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """List all posts"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts])


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get post details by ID"""
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


@app.route('/api/posts', methods=['POST'])
def create_post():
    """Create a new post"""
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content') or not data.get('user_id'):
        return jsonify({'error': 'Title, content, and user_id are required'}), 400
    
    # Verify user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    post = Post(
        title=data['title'],
        content=data['content'],
        user_id=data['user_id']
    )
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify(post.to_dict()), 201


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a post by ID"""
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    
    db.session.commit()
    
    return jsonify(post.to_dict())


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by ID"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': f'Post {post_id} deleted successfully'})


# ============================================================================
# API Routes - Statistics
# ============================================================================

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get general statistics"""
    total_users = User.query.count()
    total_posts = Post.query.count()
    
    # Get most active user
    most_active_user = None
    users = User.query.all()
    if users:
        most_active = max(users, key=lambda u: len(u.posts))
        if len(most_active.posts) > 0:
            most_active_user = {
                'username': most_active.username,
                'post_count': len(most_active.posts)
            }
    
    # Get recent posts
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    
    # Get posts per user
    posts_per_user = []
    for user in users:
        posts_per_user.append({
            'username': user.username,
            'post_count': len(user.posts)
        })
    
    return jsonify({
        'total_users': total_users,
        'total_posts': total_posts,
        'most_active_user': most_active_user,
        'recent_posts': [{'id': p.id, 'title': p.title, 'author': p.author.username} for p in recent_posts],
        'posts_per_user': posts_per_user
    })


# ============================================================================
# Health Check
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})


# ============================================================================
# Database Initialization
# ============================================================================

def init_db():
    """Initialize the database tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == '__main__':
    # Initialize database tables
    init_db()
    
    # Run the development server
    print("Starting Blog API Server...")
    print("API available at: http://localhost:5000/api")
    print("Health check: http://localhost:5000/api/health")
    app.run(debug=True, host='0.0.0.0', port=5000)
