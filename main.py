from bottle import route, get, run, template, static_file, post, request
import os.path
from pykeepass import PyKeePass

# password error management
from pykeepass.exceptions import CredentialsError

kp = PyKeePass('ressources/Database.kdbx', password='password')

group = kp.find_groups(name='New Group1', first=True)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

@route('/')
def index():
    return template('login')

@route('/ressources/<path:path>')
def callback(path):
    return static_file(path, root="./ressources/")

@get('/login')
def login():
    return template('login')

@route('/login', method='POST')
def do_login():
    nameDB = request.forms.get('nameDB')
    inputPassword = request.forms.get('inputPassword')
    if not os.path.exists('./ressources/' + str(nameDB)):
        return str(nameDB)
    else:
        try:
            kp = PyKeePass('./ressources/' + str(nameDB), password=inputPassword)
            return 'Welcome'
        except (RuntimeError, TypeError, NameError, CredentialsError):
            return 'Password not valid'


run(host='localhost', port=8088, reloader=True, debug=True)