import os
import uuid
import psycopg2
import psycopg2.extras
from flask import Flask, session, render_template, request
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

messages = [{'text':'test', 'name':'testName'}]
searchMsg = [{'text':'test', 'name':'testName'}]
users = {}
rooms = ["Pizza Room", "Soda Room", "Noodle Room"]
global currentRoom
global subList

def connectToDB():
    
    connectionString = 'dbname=messages user=postgres password=asdf host=localhost'
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")

def updateRoster():
    
    names = []
    for user_id in  users:
        print users[user_id]['username']
        if len(users[user_id]['username'])==0:
            names.append('Anonymous')
        else:
            names.append(users[user_id]['username'])
    print 'broadcasting names'
    emit('roster', names, broadcast=True)
    
def updateRooms():
    
    emit('rooms', rooms)


@socketio.on('connect', namespace='/chat')
def test_connect():
    
        print 'made it in connect'
        
        global currentRoom
        currentRoom = "Pizza Room"
        global subList
        subList = ''
        session['uuid']=uuid.uuid1()
        session['username']='starter name'
        print 'connected'
        
        users[session['uuid']]={'username':'New User'}
        if session['uuid'] in users:
            del users[session['uuid']]
            
        updateRoster()
        updateRooms()
        
        del messages[:]
        for message in messages:
            emit('message', message)

@socketio.on('moveRoom', namespace='/chat')
def move_Room(chatRoom):
    
    cRoom = chatRoom
    global currentRoom
    if subList.find(cRoom) >=1:
        if cRoom != currentRoom:
            currentRoom = cRoom
            emit('clear')
            conn = connectToDB()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            try:
                if currentRoom == "Pizza Room":
                    query = "SELECT message, username FROM pizzaRoom"
                elif currentRoom == "Soda Room":
                    query = "SELECT message, username FROM sodaRoom"
                elif currentRoom == "Noodle Room":
                    query = "SELECT message, username FROM noodleRoom"
                
                cur.execute(query)
                rows = cur.fetchall()
                conn.commit()
                cur.close()
                conn.close()
                
                del messages[:]
                for row in rows:
                    str = '***'
                    row = str.join(row)
                    t = row.partition("***")
                    tmp = {'text':t[0], 'name':t[2]}
                    messages.append(tmp)
                    
                for message in messages:
                    emit('message', message)
                    
            except:
                print("Error: Cannot select messages")
                
    else:
        emit('setDefault', currentRoom)
        emit('clear')
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            if currentRoom == "Pizza Room":
                query = "SELECT message, username FROM pizzaRoom"
            elif currentRoom == "Soda Room":
                query = "SELECT message, username FROM sodaRoom"
            elif currentRoom == "Noodle Room":
                query = "SELECT message, username FROM noodleRoom"
            
            cur.execute(query)
            rows = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
            
            del messages[:]
            for row in rows:
                str = '***'
                row = str.join(row)
                t = row.partition("***")
                tmp = {'text':t[0], 'name':t[2]}
                messages.append(tmp)
                
            for message in messages:
                emit('message', message)
                
        except:
            print("Error: Cannot select messages")
            

@socketio.on('message', namespace='/chat')
def new_message(message):
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    try:
        #tmp = {'text':message, 'name':'testName'}
        tmp = {'text':message, 'name':users[session['uuid']]['username']}
        
        if currentRoom == "Pizza Room":
            query = "INSERT INTO pizzaRoom VALUES (%s, %s) "
        elif currentRoom == "Soda Room":
            query = "INSERT INTO sodaRoom VALUES (%s, %s) "
        elif currentRoom == "Noodle Room":
            query = "INSERT INTO noodleRoom VALUES (%s, %s) "
        cur.execute(query, (message, users[session['uuid']]['username']))
        conn.commit()
        cur.close()
        conn.close()
        messages.append(tmp)
        emit('message', tmp, broadcast=True)
    except:
        print("Error: Cannot insert message")
        
@socketio.on('search', namespace='/chat')
def new_search(search):
    
    if search!='':
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            search = '%'+search+'%'
            
            if subList.find("Pizza Room") >= 1 and subList.find("Soda Room") < 1 and subList.find("Noodle Room") < 1:
                query = "SELECT message, username FROM pizzaRoom WHERE message LIKE '%s'" % (search)
            elif subList.find("Pizza Room") >= 1 and subList.find("Soda Room") >= 1 and subList.find("Noodle Room") < 1:
                query = "SELECT message, username FROM sodaRoom WHERE message LIKE '%s' UNION SELECT message, username FROM pizzaRoom WHERE message LIKE '%s'" % (search, search)
            elif subList.find("Pizza Room") >= 1 and subList.find("Soda Room") >= 1 and subList.find("Noodle Room") >= 1:
                query = "SELECT message, username FROM sodaRoom WHERE message LIKE '%s' UNION SELECT message, username FROM pizzaRoom WHERE message LIKE '%s' UNION SELECT message, username FROM noodleRoom WHERE message LIKE '%s'" % (search, search, search)
                
            cur.execute(query)
            rows = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
           
            del searchMsg[:]
            for row in rows:
               str = '***'
               row = str.join(row)
               t = row.partition("***")
               tmp = {'text':t[0], 'name':t[2]}
               searchMsg.append(tmp)
               
            for message in searchMsg:
                emit('search', message)
        
        except:
            print("Error: Cannot search message")
    
@socketio.on('identify', namespace='/chat')
def on_identify(message):
    
    print 'identify' + message
    users[session['uuid']]={'username':message}
    updateRoster()
    
@socketio.on('login', namespace='/chat')
def on_login(pw):
    
    updateRoster()
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM users WHERE username LIKE '%s' AND password LIKE '%s' " % (users[session['uuid']]['username'], pw)
    cur.execute(query)
    results = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    
    if results == []:
        emit('login')
    elif results!=[]:
        emit('run')
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            query = "SELECT pizzaRoomSub, sodaRoomSub, noodleRoomSub FROM users WHERE username LIKE '%s' " % (users[session['uuid']]['username'])
            cur.execute(query)
            result = cur.fetchall()
            rooms = []
            for theResult in result:
                str = ','
                theResult = str.join(theResult)
                rooms.append(theResult)
                
            userA = ['True,False,False']
            userB = ['True,True,False']
            userC = ['True,True,True']
            
            global subList
            subList = ''
            if rooms == userA:
                subList = " Pizza Room"
            elif rooms == userB:
                subList = " Pizza Room, Soda Room"
            elif rooms == userC:
                subList = " Pizza Room, Soda Room, Noodle Room"
            conn.commit()
            cur.close()
            conn.close()
            
        except:
            print("Error: Cannot select sub room")
        
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            query = "SELECT message, username FROM pizzaRoom"
            
            cur.execute(query)
            rows = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
            
            del messages[:]
            for row in rows:
                str = '***'
                row = str.join(row)
                t = row.partition("***")
                tmp = {'text':t[0], 'name':t[2]}
                messages.append(tmp)
                
            for message in messages:
                emit('message', message)
            
        except:
            print("Error: Cannot select messages")
    
@socketio.on('disconnect', namespace='/chat')
def on_disconnect():
    print 'disconnect'
    if session['uuid'] in users:
        del users[session['uuid']]
        updateRoster()

@app.route('/')
def hello_world():
    print 'in hello world'
    return app.send_static_file('index.html')
    return 'Hello World!'

@app.route('/js/<path:path>')
def static_proxy_js(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('js', path))
    
@app.route('/css/<path:path>')
def static_proxy_css(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('css', path))
    
@app.route('/img/<path:path>')
def static_proxy_img(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('img', path))
    
if __name__ == '__main__':
    print "A"

    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))