from lib.database import session
from lib.models import User, Password
from lib.utils import encrypt_password
from lib.database import engine, SessionLocal, Base, User, Password, Category


def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            add_password()
        elif choice == '2':
            delete_password()
        elif choice == '3':
            view_passwords()
        elif choice == '4':
            update_password()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please choose a valid option.")

def print_menu():
    print("=======Password Manager Application=======")
    print("1. Add Password")
    print("2. Delete Password")
    print("3. View Passwords")
    print("4. Update Password")
    print("5. Quit")

def add_password():
    print("Enter username:", end=" ")
    username = input()
    print("Enter email:", end=" ")
    email = input()
    print("Enter master password:", end=" ")
    master_password = input()

    user = session.query(User).filter_by(username=username).first()

    if not user:
        user = User(username=username, email=email, master_password_hash=master_password)
        session.add(user)
        session.commit()

    print("Enter website:", end=" ")
    website = input()
    print("Enter password:", end=" ")
    password = input()

    print("Enter category ID:", end=" ")
    category_id = input()

    encrypted_password = encrypt_password(password, user.master_password_hash)

    new_password = Password(
        website=website,
        username=username,
        encrypted_password=encrypted_password,
        category_id=category_id,
        user_id=user.id
    )

    session.add(new_password)
    session.commit()
    print("Password added successfully!")


def delete_password():
    username = input("Enter your username: ")
    user = session.query(User).filter_by(username=username).first()

    if user:
        passwords = session.query(Password).filter_by(user=user).all()
        if passwords:
            print(f"Passwords for user '{username}':")
            for password in passwords:
                print(f"ID: {password.id}, Website: {password.website}")

            password_id_to_delete = int(input("Enter the password ID to delete: "))
            password_to_delete = session.query(Password).filter_by(id=password_id_to_delete, user=user).first()

            if password_to_delete:
                session.delete(password_to_delete)
                session.commit()

                print(f"Password for '{password_to_delete.website}' deleted successfully for user {username}.")
            else:
                print("Invalid password ID or the password does not belong to the specified user.")
        else:
            session.delete(user)
            session.commit()
            print(f"No passwords found for user '{username}'. User '{username}' deleted.")
    else:
        print(f"User '{username}' not found.")

def view_passwords():
    username = input("Enter username to view passwords: ")
    user = session.query(User).filter_by(username=username).first()

    if user:
        passwords = session.query(Password).filter_by(user=user).all()
        if passwords:
            print(f"Passwords for user '{username}':")
            for password in passwords:
                print(f"ID: {password.id}, Website: {password.website}")
        else:
            print(f"No passwords found for user '{username}'.")
    else:
        print(f"User '{username}' not found.")

def update_password():
    username = input("Enter username to update passwords: ")
    user = session.query(User).filter_by(username=username).first()

    if user:
        passwords = session.query(Password).filter_by(user=user).all()

        if passwords:
            print(f"Passwords for user '{username}':")
            for password in passwords:
                print(f"ID: {password.id}, Website: {password.website}")

            password_id_to_update = int(input("Enter the password ID to update: "))
            password_to_update = session.query(Password).filter_by(id=password_id_to_update, user=user).first()

            if password_to_update:
                new_website = input("Enter new website (press Enter to keep the existing website): ")
                new_password = input("Enter new password (press Enter to keep the existing password): ")

                if new_website:
                    password_to_update.website = new_website

                if new_password:
                    password_to_update.encrypted_password = encrypt_password(new_password, user.master_password_hash)

                session.commit()
                print(f"Password for '{password_to_update.website}' updated successfully.")
            else:
                print("Invalid password ID or the password does not belong to the specified user.")
        else:
            print(f"No passwords found for user '{username}'.")
    else:
        print(f"User '{username}' not found.")

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)

    main()
