import click
from .database import Session
from .models import User, Password
from .utils import encrypt_password

@click.group()
def cli():
    """
    Password Manager CLI
    """
    pass

@cli.command()
@click.option('--username', prompt='Enter username', help='Username for the account')
@click.option('--website', prompt='Enter website', help='Website for the password')
@click.option('--password', prompt='Enter password', hide_input=True, confirmation_prompt=True, help='Password for the account')
def add_password(username, website, password):
    """
    Add a new password to the password manager.
    """
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        encrypted_password = encrypt_password(password, user.master_password_hash)
        new_password = Password(user_id=user.id, website=website, encrypted_password=encrypted_password)
        session.add(new_password)
        session.commit()
        click.echo('Password added successfully!')
    else:
        click.echo('User not found. Please register first.')

if __name__ == '__main__':
    cli()
