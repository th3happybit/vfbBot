
from browser import Browser
from group import Group
import websocket
import time
import json
browser = Browser()
idnotfound = '{"command":"","report":"id not found :( !"}'
def output(ws,string):
    print(string)
    ws.send(string)
def on_message(ws, command):
    text_data_json = json.loads(command)
    command = text_data_json['command']
    if 'run' in command:
        output(ws,'{"command":"","report":"runing ..."}')
        browser.navigate(
        url='https://www.facebook.com',
        wait_for='facebook',
        error='Unable to load the Facebook website'
        )
        browser.enter_login_details(email='giantscrusher@gmail.com', password='whiteHole=x=2x=3x=4x')
        output(ws,'{"command":"","report":"run operation done !"}')
    elif 'join' in command:
        output(ws,'{"command":"","report":"join ..."}')
        id = command.split(' ')[1]
        if id is not None:
            browser.joinGroup(id)
    elif 'init' in command:
        output(ws,'{"command":"","report":"init ..."}')
        id = command.split(' ')[1]
        if id is not None:
            group = Group(id)
            if group.init():
                output(ws,'{"command":"","report":"group -> id: '+id+' init operation done!"}')
            else:
                output(ws,'{"command":"","report":"group -> id: '+id+' init operation failed!"}')
        else:
            output(ws,idnotfound)
    elif 'update' in command:
        output(ws,'{"command":"","report":"update ..."}')
        id = command.split(' ')[1]
        if id is not None:
            oldgroup = Group(id)
            if group.init():
                output(ws,'{"command":"","report":"group -> id: '+id+' init operation done!"}')
                newgroup = Group(id)
                browser.getPostsv2(newgroup)
                if group.update(newgroup):
                    output(ws,'{"command":"","report":"group -> id: '+id+' updated operation done!"}')
                    output(ws,'{"command":"","report":"saving to xml ..."}')
                    group.toXml()
                else:
                    output(ws,'{"command":"","report":"group -> id: '+id+' update operation failed!"}')
            else:
                output(ws,'{"command":"","report":"group -> id: '+id+' init operation failed!"}')
        else:
            output(ws,idnotfound)
    elif 'subscribe' in command:
        output(ws,'{"command":"","report":"subscribe ..."}')
        id = command.split(' ')[1]
        if id is not None:
            group = Group(id)
            if not group.init():
                browser.getPostsv2(group)
                glen = len(group.posts)
                if glen > 0:
                    output(ws,'{"command":"","report":"getting posts done ! total ( '+glen+' )","len":"'+glen+'"}')
                    if group.toXml():
                        output(ws,'{"command":"","report":"group saved !"}')
                else:
                    output(ws,'{"command":"","report":":( 0 posts find"}')
            else:
                output(ws,'{"command":"","report":"group already subscribed ! :p "}')
        else:
            output(ws,idnotfound)
    elif 'list' in command:
        output(ws,'{"command":"","report":"getting list ..."}')
        groupslist = browser.listgroups()
        for group in groupslist:
            output(ws,'{"command":"","report":"-'+group+'"}')
    elif 'delete' in command:
        id = command.split(' ')[1]
        if id is not None and not (id == 'all'):
            group = Group(id)
            if group.delete():
                output(ws,'{"command":"","report":"group -> id : '+ id +' delete !"}')
            else:
                output(ws,'{"command":"","report":"group -> id : '+ id +' removal failed !"}')
        elif 'delete all' in command:
            gl = browser.listgroups()
            if len(gl) > 0:
                for g in gl:
                    group = Group(g)
                    group.delete()
            else:
                output(ws,'{"command":"","report":"no group to delete !"}')
                return False
            gl = browser.listgroups()
            if len(gl) == 0:
                output(ws,'{"command":"","report":"all groups deleted !"}')
            else:
                output(ws,'{"command":"","report":"delete all groups failed !"}')
        else:
            output(ws,idnotfound)
def on_error(ws, error):
    output(ws,error)

def on_close(ws):
    print("### closed ###")
    # Attemp to reconnect with 2 seconds interval
    time.sleep(2)
    initiate()

def on_open(ws):
    print("### Initiating new websocket connection ###")
    time.sleep(1)
    ws.send('{"command":"hey","report":"Bot started"}')
def initiate():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/ws/controll/testing/",
        on_message = on_message,
        on_error = on_error,
        on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == '__main__':
    initiate()
