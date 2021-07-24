import base64
from configparser import ConfigParser
import bcrypt

import Cred
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Global Variables
filepath = f'{os.getcwd()}/CredManager'
masterSection = 'master'
cipherSection = 'cipher'


def hash_it(some_string: str) -> str:
    byte_string = some_string.encode()
    hashed = bcrypt.hashpw(byte_string, bcrypt.gensalt())
    return hashed.decode()


def encrypt_it(some_string: str, cipher: bytes):
    f = Fernet(cipher)
    return f.encrypt(some_string.encode())


def decrypt_it(some_string: str, cipher: bytes):
    f = Fernet(cipher)
    return f.decrypt(some_string.encode())


def create_master(username: str, password: str) -> bool:
    with open(f'{filepath}/{username}.ini', 'w+') as f:
        parser = ConfigParser()
        parser['master'] = {'Username': hash_it(username), 'Password': hash_it(password)}
        parser.write(f)

    if os.path.exists(f'{filepath}/{username}.ini'):
        return True
    else:
        return False


def gen_cipher(username: str, password: str):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=username.encode(),
        iterations=100000, )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    parser = ConfigParser()
    parser.read(f'{filepath}/{username}.ini')
    parser.set(masterSection, 'cipher', key.decode())
    with open(f'{filepath}/{username}.ini', 'w') as f:
        parser.write(f)


def check_master(master_username: str, master_password: str) -> bool:
    """Checks the input password provided by the user with the stored hash and :returns True or False."""

    # create a parser
    parser = ConfigParser()

    # read config file
    parser.read(f'{filepath}/{master_username}.ini')

    # getting the master password and comparing it with the input password
    if parser.has_section(masterSection):
        master_hash = parser[masterSection]['Password']

        # checking whether the input password and stored hash are equal
        if bcrypt.checkpw(master_password.encode(), master_hash.encode()):
            print('Welcome')
            return True
        else:
            print('Sorry. please enter correct password')
            return False
    else:
        print('Sorry!! please enter correct username')
        return False


def get_cipher_key(user: str) -> str:
    """ :returns a cipher key for encrypting and decrypting purpose's"""

    # create a parser
    parser = ConfigParser()

    # read config file
    parser.read(f'{filepath}/{user}.ini')

    if parser.has_section(masterSection):
        cipher_key = parser[masterSection]['cipher']
        return cipher_key

    else:
        raise Exception('Section {0} not found in the {1} file'.format(masterSection, filepath))


def new_cred(username: str, cred: Cred):
    cipher = get_cipher_key(username)
    with open(f'{filepath}/{username}.ini', 'a') as f:
        parser = ConfigParser()
        parser[cred.app_name] = {'App Name': cred.app_name,
                                 'Username': encrypt_it(cred.app_username, cipher.encode()).decode(),
                                 'Password': encrypt_it(cred.app_password, cipher.encode()).decode(),
                                 'URL': cred.app_url
                                 }
        parser.write(f)
        print(f'Cred for {cred.app_name} created successfully')


def get_cred(username: str):
    app_name = input('Enter App Name')
    cipher = get_cipher_key(username)
    # create a parser
    parser = ConfigParser()

    # read config file
    parser.read(f'{filepath}/{username}.ini')

    # getting the master password and comparing it with the input password
    if parser.has_section(app_name):
        app_username = decrypt_it(parser[app_name]['username'], cipher.encode()).decode()
        app_password = decrypt_it(parser[app_name]['password'], cipher.encode()).decode()
        app_url = parser[app_name]['url']
        print("!!" * 25)
        print("Application Name: " + app_name)
        print("Username: " + app_username)
        print("Password: " + app_password)
        print("URL: " + app_url)
        print("!!" * 25)
    else:
        print('Enter valid App name')