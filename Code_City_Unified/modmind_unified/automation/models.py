import logging

"""
Database models for Automation DNA
SQLAlchemy models for process persistence
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Initialize SQLAlchemy
db = SQLAlchemy()


class ProcessDNA(db.Model):
    """Database model for Process DNA"""
    
    __tablename__ = 'process_dna'
    
    id = db.Column(db.Integer, primary_key=True)
    dna_id = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    process_type = db.Column(db.String(50), nullable=False)
    data = db.Column(db.JSON, nullable=False)  # Full DNA data as JSON
    fitness_score = db.Column(db.Float, default=0.0)
    generation = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProcessDNA {self.name} (gen {self.generation})>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'dna_id': self.dna_id,
            'name': self.name,
            'description': self.description,
            'process_type': self.process_type,
            'fitness_score': self.fitness_score,
            'generation': self.generation,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def get_dna_object(self):
        """Convert stored JSON data back to ProcessDNA object"""
        from automation_dna.core.dna_process import ProcessDNA as CoreProcessDNA
        return CoreProcessDNA.from_dict(self.data)


class User(db.Model):
    """Database model for Users"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }


class EvolutionSession(db.Model):
    """Database model for Evolution Sessions"""
    
    __tablename__ = 'evolution_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='running')  # running, paused, completed
    current_generation = db.Column(db.Integer, default=0)
    population_size = db.Column(db.Integer, default=50)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('sessions', lazy=True))
    
    def __repr__(self):
        return f'<EvolutionSession {self.name} (gen {self.current_generation})>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'current_generation': self.current_generation,
            'population_size': self.population_size,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class MarketplaceListing(db.Model):
    """Database model for Marketplace Listings"""
    
    __tablename__ = 'marketplace_listings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    process_id = db.Column(db.Integer, db.ForeignKey('process_dna.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, default=0.0)
    category = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.JSON, nullable=True)  # Array of tags
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('listings', lazy=True))
    process = db.relationship('ProcessDNA', backref=db.backref('listings', lazy=True))
    
    def __repr__(self):
        return f'<MarketplaceListing {self.title} (${self.price})>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'process_id': self.process_id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'tags': self.tags,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Transaction(db.Model):
    """Database model for Marketplace Transactions"""
    
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('marketplace_listings.id'), nullable=False)
    process_id = db.Column(db.Integer, db.ForeignKey('process_dna.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='completed')  # pending, completed, refunded
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref=db.backref('purchases', lazy=True))
    seller = db.relationship('User', foreign_keys=[seller_id], backref=db.backref('sales', lazy=True))
    listing = db.relationship('MarketplaceListing', backref=db.backref('transactions', lazy=True))
    process = db.relationship('ProcessDNA', backref=db.backref('transactions', lazy=True))
    
    def __repr__(self):
        return f'<Transaction {self.id} (${self.amount})>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'buyer_id': self.buyer_id,
            'seller_id': self.seller_id,
            'listing_id': self.listing_id,
            'process_id': self.process_id,
            'amount': self.amount,
            'status': self.status,
            'transaction_date': self.transaction_date.isoformat()
        }


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
        logging.info("✅ Database initialized successfully!")


def get_or_create_user(username, email, password_hash):
    """Get existing user or create new one"""
    user = User.query.filter_by(email=email).first()
    if user:
        return user
    
    # Create new user
    user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )
    db.session.add(user)
    db.session.commit()
    return user


def save_process_dna(process_dna):
    """Save ProcessDNA to database"""
    # Convert to dict for storage
    process_data = process_dna.to_dict()
    
    # Create database record
    db_process = ProcessDNA(
        dna_id=process_data['dna_id'],
        name=process_data['name'],
        description=process_data.get('description', ''),
        process_type=process_data['process_type'],
        data=process_data,
        fitness_score=process_data.get('fitness_score', 0.0),
        generation=process_data.get('generation', 1)
    )
    
    db.session.add(db_process)
    db.session.commit()
    
    return db_process


def get_process_dna(dna_id):
    """Get ProcessDNA from database"""
    db_process = ProcessDNA.query.filter_by(dna_id=dna_id).first()
    if db_process:
        return db_process.get_dna_object()
    return None


def get_all_processes(user_id=None):
    """Get all processes, optionally filtered by user"""
    query = ProcessDNA.query
    if user_id:
        # In a real implementation, we'd have user ownership
        # For now, just return all processes
        pass
    
    return [process.get_dna_object() for process in query.all()]


def delete_process_dna(dna_id):
    """Delete ProcessDNA from database"""
    db_process = ProcessDNA.query.filter_by(dna_id=dna_id).first()
    if db_process:
        db.session.delete(db_process)
        db.session.commit()
        return True
    return False


# Database migration functions (simplified)
def create_database_tables():
    """Create all database tables"""
    db.create_all()
    logging.info("✅ All database tables created!")


def drop_database_tables():
    """Drop all database tables"""
    db.drop_all()
    logging.info("⚠️ All database tables dropped!")


if __name__ == "__main__":
    logging.info("🗃️ Automation DNA Database Models")
    logging.info("✅ Models defined and ready for initialization")
