#!/usr/bin/env python
"""
Update database script for Know Your Fan application.
This script updates the SQLite database schema to match the current models.
"""

import os
import sys
from flask import Flask
from sqlalchemy import inspect, text
from models import db, User, Profile, Document, SocialAccount, EsportsProfile

def create_app():
    """Create and configure the Flask app for database migration"""
    app = Flask(__name__, instance_relative_config=True)
    
    # Make sure we use an absolute path to the database
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'instance', 'knowyourfan.db'))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Ensure instance path exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    db.init_app(app)
    return app

def get_table_columns(table_name, inspector):
    """Get existing columns for a table"""
    columns = []
    try:
        columns = [column['name'] for column in inspector.get_columns(table_name)]
    except Exception as e:
        print(f"Error getting columns for {table_name}: {e}")
    return columns

def add_missing_columns(table_name, existing_columns, expected_columns, connection):
    """Add missing columns to a table"""
    missing_columns = [col for col in expected_columns if col[0] not in existing_columns]
    
    if not missing_columns:
        print(f"No missing columns in {table_name} table.")
        return
    
    print(f"Adding missing columns to {table_name} table: {[col[0] for col in missing_columns]}")
    
    for column_name, column_type in missing_columns:
        try:
            # SQLite has limited ALTER TABLE support, but ALTER TABLE ADD COLUMN works
            connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"))
            print(f"Added column {column_name} to {table_name} table.")
        except Exception as e:
            print(f"Error adding column {column_name} to {table_name} table: {e}")

def update_database(app):
    """Update the database schema"""
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    with app.app_context():
        # Check if tables exist
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        print(f"Existing tables: {existing_tables}")
        
        if not existing_tables:
            print("No tables found. Creating all tables...")
            db.create_all()
            return
        
        # Define expected columns for each table
        expected_columns = {
            'user': [
                ('id', 'INTEGER'), 
                ('username', 'VARCHAR(80)'),
                ('email', 'VARCHAR(120)'),
                ('password_hash', 'VARCHAR(128)'),
                ('name', 'VARCHAR(100)'),
                ('address', 'VARCHAR(200)'),
                ('cpf', 'VARCHAR(14)'),
                ('birth_date', 'DATE'),
                ('created_at', 'DATETIME')
            ],
            'profile': [
                ('id', 'INTEGER'),
                ('user_id', 'INTEGER'),
                ('interests', 'TEXT'),
                ('fan_story', 'TEXT'),
                ('favorite_games', 'TEXT'),
                ('other_games', 'TEXT'),
                ('favorite_teams', 'TEXT'),
                ('other_teams', 'TEXT'),
                ('events_attended', 'TEXT'),
                ('other_events', 'TEXT'),
                ('purchases', 'TEXT'),
                ('profile_picture', 'VARCHAR(255)')
            ],
            'document': [
                ('id', 'INTEGER'),
                ('user_id', 'INTEGER'),
                ('filename', 'VARCHAR(255)'),
                ('doc_type', 'VARCHAR(50)'),
                ('upload_date', 'DATETIME'),
                ('verified', 'BOOLEAN'),
                ('verification_date', 'DATETIME')
            ],
            'social_account': [
                ('id', 'INTEGER'),
                ('user_id', 'INTEGER'),
                ('platform', 'VARCHAR(50)'),
                ('account_id', 'VARCHAR(255)'),
                ('username', 'VARCHAR(100)'),
                ('access_token', 'TEXT'),
                ('token_expiry', 'DATETIME'),
                ('last_sync', 'DATETIME')
            ],
            'esports_profile': [
                ('id', 'INTEGER'),
                ('user_id', 'INTEGER'),
                ('platform', 'VARCHAR(50)'),
                ('profile_url', 'VARCHAR(255)'),
                ('username', 'VARCHAR(100)'),
                ('verified', 'BOOLEAN'),
                ('relevance_score', 'FLOAT'),
                ('verified_date', 'DATETIME')
            ]
        }
        
        # Update each table
        with db.engine.connect() as connection:
            print("Checking and updating database schema...")
            
            for table_name, columns in expected_columns.items():
                if table_name in existing_tables:
                    existing_columns = get_table_columns(table_name, inspector)
                    print(f"Table {table_name} has columns: {existing_columns}")
                    add_missing_columns(table_name, existing_columns, columns, connection)
                else:
                    print(f"Table '{table_name}' doesn't exist. Creating...")
                    # For missing tables, we'll let SQLAlchemy create them with db.create_all()
            
            # This will create any missing tables
            db.create_all()
            
            print("Database schema update completed!")

if __name__ == "__main__":
    app = create_app()
    update_database(app)
    print("Database update complete!")