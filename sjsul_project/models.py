from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association tables for many-to-many relationships
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)


class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    audit_logs = relationship('AuditLog', back_populates='user')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def has_permission(self, resource, action):
        """Check if user has a specific permission through their roles"""
        for role in self.roles:
            for permission in role.permissions:
                if permission.resource == resource and permission.action == action:
                    return True
        return False
    
    # Flask-Login required properties
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return self.active
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)


class Role(Base):
    """Role model for RBAC"""
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    
    # Relationships
    users = relationship('User', secondary=user_roles, back_populates='roles')
    permissions = relationship('Permission', secondary=role_permissions, back_populates='roles')
    
    def __repr__(self):
        return f'<Role {self.name}>'


class Permission(Base):
    """Permission model for fine-grained access control"""
    __tablename__ = 'permissions'
    
    id = Column(Integer, primary_key=True)
    resource = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)
    
    # Relationships
    roles = relationship('Role', secondary=role_permissions, back_populates='permissions')
    
    def __repr__(self):
        return f'<Permission {self.action} on {self.resource}>'


class AuditLog(Base):
    """Audit log for tracking security events"""
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    action = Column(String(50), nullable=False)
    resource = Column(String(100), nullable=True)
    result = Column(String(20), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship('User', back_populates='audit_logs')
    
    def __repr__(self):
        return f'<AuditLog {self.action} by user {self.user_id} - {self.result}>'