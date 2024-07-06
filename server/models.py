from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()
import re

def validate_clickbait(title):
    clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
    if not any(phrase in title for phrase in clickbait_phrases):
        raise ValueError(f'Title must contain one of the following phrases: {", ".join(clickbait_phrases)}')

def validate_category(category):
    if category not in ['Fiction', 'Non-Fiction']:
        raise ValueError('Category must be either Fiction or Non-Fiction')

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Author name cannot be empty.')
        if Author.query.filter(Author.name == name).first():
            raise ValueError('An author with this name already exists.')
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not re.match(r'^\d{10}$', phone_number):
            raise ValueError('Phone number must be exactly 10 digits.')
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  

    @validates('title')
    def validate_title(self, key, title):
        validate_clickbait(title)
        return title

    @validates('category')
    def validate_category(self, key, category):
        validate_category(category)
        return category

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content must be at least 250 characters long.')
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary must be a maximum of 250 characters.')
        return summary

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'