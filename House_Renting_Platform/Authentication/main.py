from auth.auth_logic import signup, login

print("Welcome!")
choice = input("Do you want to [signup] or [login]? ").strip().lower()

if choice == "signup":
    signup()
elif choice == "login":
    login()
else:
    print("Invalid choice.")
