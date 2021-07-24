class Cred:

    def __init__(self, app_name: str, app_username: str, app_password: str, app_url=''):
        self.app_name = app_name
        self.app_username = app_username
        self.app_password = app_password
        self.app_url = app_url

    def __str__(self):
        print("Application Name: "+self.app_name)
        print("Username: "+self.app_username)
        print("Password: "+self.app_password)
        print("URL: "+self.app_url)