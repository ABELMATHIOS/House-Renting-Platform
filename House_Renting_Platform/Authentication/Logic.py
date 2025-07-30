from .models import load_users, save_users
from .hash_utils import hash_password, check_password

def signup():
    users = load_users()
    username = input("Choose a username: ").strip()
    if username in users:
        print("Username already exists!")
        return

    password = input("Choose a password: ").strip()
    users[username] = hash_password(password)
    save_users(users)
    print("Signup successful!")

def login():
    users = load_users()
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username not in users:
        print("User not found.")
        return

    if check_password(password, users[username]):
        print("Login successful!")
    else:
        print("Incorrect password.")
