from bottle import route, get, run, template, static_file, post, request
import os.path
from pykeepass import PyKeePass

# password error management
from pykeepass.exceptions import CredentialsError


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

#Routage de tout ce qui référencé dans le dossier "ressources" vers le tout ce qui dans le dossier local "ressources"
@route('/ressources/<path:path>')
def callback(path):
    return static_file(path, root="./ressources/")

#Routage de /login vers la page de connexion
@route('/login')
def login():
    return template('login', loginError = '')

#Routage de /login vers la page de connexion AVEC LA METHODE POST
@post('/login')
def do_login():
    nameDB = request.forms.get('nameDB')
    inputPassword = request.forms.get('inputPassword')
    if not os.path.exists('./ressources/' + str(nameDB)):
        return template('login', loginError='<div class="alert alert-danger" role="alert">Please enter a correct filename (with extension)</div>')
    else:
        try:
            kp = PyKeePass('./ressources/' + str(nameDB), password=inputPassword)
            entries='<table class="table table-striped"><thead><tr><th scope="col">Title</th><th scope="col">Username</th></tr></thead><tbody>'
            for entry in kp.entries:
                x = str(entry).split('"', 1)
                x = str(x[1]).split('(', 1)
                title = str(x[0])
                username = str(x[1]).split(')', 1)
                entries+="<tr><td>" + str(title) + "</td><td>" + str(username[0]) + "</td></tr>"
            entries+="</tbody></table>"
            return template('index', welcomeMsg='<div class="alert alert-success" id="success-alert" role="alert">Welcome to the Datadabase editing interface!<button type="button" class="close" data-dismiss="alert">x</button></div>', dbEntries=entries)
        except (RuntimeError, TypeError, NameError, CredentialsError):
            return template('login', loginError='<div class="alert alert-danger" role="alert">Please enter a correct password</div>')


run(host='localhost', port=8088, reloader=True, debug=True)