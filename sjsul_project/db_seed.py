#!/usr/bin/env python3
"""Database seeding script for SJSUL project"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Role, Permission
from security import hash_password, verify_password
import os

# Remove existing database
if os.path.exists('sjsul.db'):
    os.remove('sjsul.db')
    print('Removed existing database')

# Create engine and session
engine = create_engine('sqlite:///sjsul.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

print('Created database tables')

# Create Permissions
permissions_data = [
    ('books', 'read', 'View library books catalog'),
    ('books', 'write', 'Add or edit books'),
    ('books', 'delete', 'Remove books from catalog'),
    ('users', 'manage', 'Manage user accounts'),
    ('reports', 'read', 'View administrative reports'),
    ('audit', 'read', 'View audit logs'),
]

permissions = {}
for resource, action, desc in permissions_data:
    perm = Permission(resource=resource, action=action)
    session.add(perm)
    permissions[f'{resource}:{action}'] = perm

session.commit()
print(f'Created {len(permissions_data)} permissions')

# Create Roles
admin_role = Role(
    name='Admin',
    description='Full system access - can manage users and view all resources'
)
admin_role.permissions.extend([
    permissions['books:read'],
    permissions['books:write'],
    permissions['books:delete'],
    permissions['users:manage'],
    permissions['reports:read'],
    permissions['audit:read'],
])

librarian_role = Role(
    name='Librarian',
    description='Can manage books and view reports'
)
librarian_role.permissions.extend([
    permissions['books:read'],
    permissions['books:write'],
    permissions['reports:read'],
])

student_role = Role(
    name='Student',
    description='Can only view books catalog'
)
student_role.permissions.append(permissions['books:read'])

session.add_all([admin_role, librarian_role, student_role])
session.commit()
print('Created 3 roles: Admin, Librarian, Student')

# Create Users
# IMPORTANT: Create two users with the same password to demonstrate different hashes
test_password = 'Password123!'

users_data = [
    ('admin', 'admin@sjsu.edu', test_password, 'Admin', True),
    ('librarian', 'librarian@sjsu.edu', 'LibPass456', 'Librarian', True),
    ('student1', 'student1@sjsu.edu', test_password, 'Student', True),  # Same password as admin
    ('student2', 'student2@sjsu.edu', 'StudPass789', 'Student', True),
    ('disabled_user', 'disabled@sjsu.edu', 'Disabled123', 'Student', False),  # Disabled for de-provisioning demo
]

for username, email, password, role_name, active in users_data:
    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        active=active
    )
    
    # Assign role
    role = session.query(Role).filter_by(name=role_name).first()
    if role:
        user.roles.append(role)
    
    session.add(user)

session.commit()
print(f'Created {len(users_data)} users')

admin_user = session.query(User).filter_by(username='admin').first()
student1_user = session.query(User).filter_by(username='student1').first()

print(f'\nBoth admin and student1 use password: {test_password}')
print(f'\nadmin hash:    {admin_user.password_hash}')
print(f'student1 hash: {student1_user.password_hash}')

admin_match = verify_password(test_password, admin_user.password_hash)
student_match = verify_password(test_password, student1_user.password_hash)
print(f'\nVerify admin password:    {admin_match}')
print(f'Verify student1 password: {student_match}')

print('\n' + '-' * 50)
print('Demo Credentials:')
print('\nAdmin Account:')
print('  Username: admin')
print('  Password: Password123!')
print('  Permissions: Full access to all resources\n')

print('Librarian Account:')
print('  Username: librarian')
print('  Password: LibPass456')
print('  Permissions: Manage books, view reports\n')

print('Student Account:')
print('  Username: student1')
print('  Password: Password123!')
print('  Permissions: View books only\n')

print('Disabled Account (for de-provisioning demo):')
print('  Username: disabled_user')
print('  Password: Disabled123')
print('  Status: DISABLED (cannot login)')