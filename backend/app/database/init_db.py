#!/usr/bin/env python3

"""
Database initialization script for PhantomGuard
"""

from ..database.session import engine, Base
from ..models.user import User
from ..models.log import Log
from ..models.alert import Alert

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()