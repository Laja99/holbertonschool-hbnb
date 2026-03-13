from app import db, bcrypt
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False, **kwargs):
        super().__init__(**kwargs)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        if password:
            self.hash_password(password)

    @validates('first_name')
    def validate_first_name(self, key, first_name):

        if not first_name:
            raise ValueError("First name is required")
        if len(first_name) > 50:
            raise ValueError("First name cannot exceed 50 characters")
        if len(first_name) < 2:
            raise ValueError("First name must be at least 2 characters")
        return first_name.strip()
    
    @validates('last_name')
    def validate_last_name(self, key, last_name):

        if not last_name:
            raise ValueError("Last name is required")
        if len(last_name) > 50:
            raise ValueError("Last name cannot exceed 50 characters")
        if len(last_name) < 2:
            raise ValueError("Last name must be at least 2 characters")
        return last_name.strip()
    
    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    
    @validates('email')
    def validate_email(self, key, email):

        if not email:
            raise ValueError("Email is required")

        email = email.lower().strip()

        if "@" not in email:
            raise ValueError("Invalid email format: must contain @")

        local_part, domain = email.split("@")
        if not local_part or not domain:
            raise ValueError("Invalid email format: empty local part or domain")
        
        if "." not in domain:
            raise ValueError("Invalid email format: domain must contain a dot")

        if len(email) > 120:
            raise ValueError("Email cannot exceed 120 characters")

        return email

    @validates('password')
    def validate_password(self, key, password):

        if password and not password.startswith('$2b$'):
            if len(password) < 8:
                raise ValueError("Password must be at least 8 characters long")
        return password
    
    def hash_password(self, password):
        """Hashes the password before storing it"""
        if not password:
            raise ValueError("Password is required")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Verify if password matches the stored hash"""
        if not self.password:
            return False

        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Convert user object to dictionary without password"""
        data = super().to_dict()

        data.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        })

        if "password" in data:
            del data["password"]

        return data
