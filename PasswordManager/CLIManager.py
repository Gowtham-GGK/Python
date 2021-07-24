import os

import CredManager
from Cred import Cred

filepath = f'{os.getcwd()}/CredManager'

def title():
    """Title of the Credential Manager"""

    os.system('cls')
    print("**" * 25)
    print("         Welcome to GK Credential Manger")
    print("**" * 25)
    print('')


def main_menu():
    """ Display Main Menu options"""
    title()
    # print('')
    # print("--" * 25)
    print(" Menu")
    print('')
    print("1. Store new Credential")
    print("2. Get stored Credential")
    print("3. Quit")
    print("--" * 25)

    return input('Select a option: ')


def wait():
    if len(input("Enter to continue:")) > 0:
        pass


def prompt_for_master():
    master_username = input('Enter you master username')
    master_password = input('Enter your master password')
    return master_username, master_password


def prompt_for_new_user():
    print("Enter your user name: ", end='')
    user_name = input()
    print("Enter Master Password: ", end='')
    master_pwd = input()
    print("Re-Enter your Master Password: ", end='')
    re_master_pwd = input()
    while user_name == '' or master_pwd == '':
        print('Username/Password can\'t be empty')
        print("Enter your user name: ", end='')
        user_name = input()
        print("Enter Master Password: ", end='')
        master_pwd = input()
        print("Re-Enter your Master Password: ", end='')
        re_master_pwd = input()
    while master_pwd != re_master_pwd:
        print("Entered passwords didn't match")
        print("Enter Master Password: ", end='')
        master_pwd = input()
        print("Re-Enter your Master Password ", end='')
        re_master_pwd = input()
    return user_name, master_pwd


def check_existing_user():
    """ Checks whether the user already exists or not.
        If User doesn't exist , it will navigate to Register section
        If User exist, it will ask for master password"""

    print("Are you an existing user? (Y/N): ", end='')
    existing = input()

    while existing not in ['Y', 'y', 'N', 'n']:
        print("Enter a Valid input")
        print("Are you an existing user(Y/N): ", end='')
        existing = input()

    if existing in ['Y', 'y']:
        return True
    else:
        return False


def register():
    """ Registration section:
        """
    print("--" * 25)
    print("         Register/Sign-In")
    print("--" * 25)
    user_name, master_pwd = prompt_for_new_user()
    print(user_name, master_pwd)
    while os.path.exists(f'{filepath}/{user_name}.ini'):
        print('Entered username already exists. Try another username')
        print("Enter your user name: ", end='')
        user_name = input()
    CredManager.create_master(user_name, master_pwd)
    CredManager.gen_cipher(user_name, master_pwd)
    print('~~' * 25)
    print("You are registered successfully!! ")
    print('~~' * 25)
    wait()


def store_new_cred(master):
    app_name = input('Enter App Name')
    app_username = input('Enter App Username')
    app_password = input('Enter App Password')
    app_url = input('Enter App URL')
    cred = Cred(app_name, app_username, app_password, app_url)
    CredManager.new_cred(master, cred)