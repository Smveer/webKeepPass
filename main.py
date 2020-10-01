from bottle import route, run, template
from pykeepass import PyKeePass

# load database
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
    return template('index.html', name="KEEPASS WEB by Students", entries=str(group.entries))


run(host='localhost', port=8088, reloader=True)