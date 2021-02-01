from bottle import route, get, run, template, static_file, post, request
import os.path
from pykeepass import PyKeePass
from pykeepass.exceptions import CredentialsError # password error management


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


################################################################
#Routage de tout ce qui référencé dans le dossier "ressources" vers le tout ce qui dans le dossier local "ressources"
@route('/ressources/<path:path>')
def callback(path):
    return static_file(path, root="./ressources/")
################################################################


################################################################
#Routage de /home vers la page de connexion
@route('/home')
def home():
    return template('home', homeError = '')
################################################################


################################################################
#Routage de /home vers la page de connexion AVEC LA METHODE POST
@post('/home')
def do_home():
    nameDB = request.forms.get('nameDB') #recuperation du nameDB depuis home.html
    inputPassword = request.forms.get('inputPassword') #recuperation du inputPassword depuis home.html
    if not os.path.exists('./ressources/' + str(nameDB)): #cherche si le chemin n'existe pas
        return template('home', homeError='<div class="alert alert-danger" role="alert">Please enter a correct filename (with extension)</div>') #retour au home.html avec erreur si chemin n'existe pas
    else:
        try:
            global kp
            global varTab
            varTab = [[], [[], [], []]]
            kp = PyKeePass('./ressources/' + str(nameDB), password=inputPassword) #identification au keepass
            entries=""
            idUser = 0
            for entry in kp.entries: #pour chaque element (entry) de kp.entries faire:
                x = str(entry).split('"', 1)
                x = str(x[1]).split('(', 1)
                title = str(x[0]) #split pour récupérer le Title
                username = str(x[1]).split(')', 1) #split pour récupérer le Username
                password = entry.password
                varTab[0].append(idUser)
                varTab[1][0].append(title)
                varTab[1][1].append(username[0])
                varTab[1][2].append(password)
                idUser += 1
                entries+="<tr><td>" + str(title) + "</td><td>" + str(username[0]) + "</td><td class=\"password\">" + str(password) + "</td><td><a href=\"/home/entry/" + str(idUser) + "\">Manage</a></td></tr>" #concaténer ligne à chaque itération
            return template('index', welcomeMsg='<div class="alert alert-success" id="success-alert" role="alert">Welcome to the Datadabase editing interface!<button type="button" class="close" data-dismiss="alert">x</button></div>', dbEntries=entries)
        except (RuntimeError, TypeError, NameError, CredentialsError): #Si erreur lors de l'identification faire:
            return template('home', homeError='<div class="alert alert-danger" role="alert">Please enter a correct password</div>') #retour au home.html avec erreur si password pas bon
################################################################

@get('/home/groupmanager')
def groupmanager():
    groups=''
    for group in kp.groups:
        x = str(group).split('"', 1)
        x = str(x[1]).split('"', 1)
        title = str(x[0])
        groups+="<tr><td><a href='" + str(title) + "'>" + str(title) + "</a></td></tr>"
    return template('groupmanager', dbGroups=groups)

@get('/home/entry/<path:path>')
def editEntry(path):
    print('debut')
    idEntry = path
    titleEntry = varTab[1][0][int(idEntry)]
    usernameEntry = varTab[1][1][int(idEntry)]
    passwordEntry = varTab[1][2][int(idEntry)]
    print('fin')
    print(titleEntry, " ", usernameEntry, " ", passwordEntry)
    return template('entry', titleEntry = titleEntry, usernameEntry = usernameEntry, passwordEntry = passwordEntry)


@get('/home/<path:path>')
def printGroup(path):
    print(str(kp.groups))
    for group in kp.groups:
        if str(path) in str(group):
            entries=""
            for entry in kp.entries:  # pour chaque element (entry) de kp.entries faire:
                x = str(entry).split('"', 1)
                x = str(x[1]).split('(', 1)
                title = str(x[0])  # split pour récupérer le Title
                username = str(x[1]).split(')', 1)  # split pour récupérer le Username
                password = entry.password
                slash = "/"
                count = 0
                for indexSlash in title:
                    if(str(slash) == str(indexSlash)):
                        count += 1
                groupTitle = str(title).split('/', count)

                if(count == 1):
                    if(str(groupTitle[count-1]) + "/" == str(path)):
                        entries += "<tr><td>" + str(groupTitle[count]) + "</td><td>" + str(
                            username[0]) + "</td><td class=\"password\">" + str(password) + "</td></tr>" # concaténer ligne à chaque itération
                else:
                    groupname = ""
                    for i in range(count):
                        if(i == 0):
                            groupname = str(groupname) + (groupTitle[i])
                        else:
                            groupname = str(groupname) + "/" + (groupTitle[i])
                    if (str(groupname) + "/" == str(path)):
                        entries += "<tr><td>" + str(groupTitle[count]) + "</td><td>" + str(
                            username[0]) + "</td><td class=\"password\">" + str(password) + "</td></tr>" # concaténer ligne à chaque itération
            return template('group', dbEntries=entries)

run(host='localhost', port=8088, reloader=True, debug=True)