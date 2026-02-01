import bcrypt
import streamlit as st
from src.utils.database import db

class Auth:
    @staticmethod
    def hash_password(password):
        """Hash a password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(stored_hash, password):
        """Verify a password against the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

    @staticmethod
    def login(email, password):
        """Attempt to log in a user. Returns tuple (success, message/user)."""
        user = db.get_user_by_email(email)
        
        if not user:
            return False, "User not found."
            
        if Auth.verify_password(user['password_hash'], password):
            # Set session state
            st.session_state.user = {
                'id': user['id'],
                'name': user['name'],
                'email': user['email']
            }
            return True, user
        else:
            return False, "Invalid password."

    @staticmethod
    def validate_email(email):
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password(password):
        return len(password) >= 6

    @staticmethod
    def signup(name, email, password):
        """Register a new user."""
        if not name or not email or not password:
            return False, "All fields are required."
            
        if not Auth.validate_email(email):
            return False, "Invalid email format."
            
        if not Auth.validate_password(password):
            return False, "Password must be at least 6 characters."

        hashed_pw = Auth.hash_password(password)
        user_id = db.create_user(email, name, hashed_pw)
        
        if user_id:
            # Auto login after signup
            user = {
                'id': user_id,
                'email': email,
                'name': name
            }
            st.session_state.user = user
            return True, "Account created successfully."
        else:
            return False, "Email already registered."

    @staticmethod
    def delete_account():
        if 'user' in st.session_state and st.session_state.user:
            user_id = st.session_state.user['id']
            if db.delete_user(user_id):
                Auth.logout()
                return True
        return False

    @staticmethod
    def logout():
        """Clear the session."""
        if 'user' in st.session_state:
            del st.session_state.user
        st.rerun()

    @staticmethod
    def require_auth():
        """Check if user is logged in."""
        return 'user' in st.session_state
