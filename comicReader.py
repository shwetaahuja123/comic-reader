from flask import Flask, jsonify, send_file, request
from utilities import getPrevPage, getNextPage
from init import users
from loggerMiddleware import LoggerMiddleware, savedUuids
import jwt
import hashlib

# print('here', i)
app = Flask(__name__)
arr = ['Tom And Jerry', 'Lion King']

app.wsgi_app = LoggerMiddleware(app.wsgi_app)

@app.route("/health", methods=['GET'])
def health():
    return jsonify(status='Healthy'), 200

@app.route("/register", methods=['POST'])
def register():
    data = request.json
    email = data['email']
    password = data['password']
    result = hashlib.sha256(password.encode()).hexdigest()
    newUser = {email: result}

    users.update(newUser)
    filehandler = open('authDetails.txt', 'wt')
    data = str(users)
    filehandler.write(data)

    return jsonify(users)

@app.route("/login", methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    hashedpassword = hashlib.sha256(password.encode()).hexdigest()

    if(email in users and hashedpassword == users[email]):
        msg = 'User authenticated'
        key="secret1"
        encoded = jwt.encode({'email':email }, key, algorithm="HS256")

        savedUuids[str(encoded)] = email
        return jsonify(data=msg, uuid=encoded)
    else:
        msg = 'Invalid user'
        return jsonify(data=msg)

@app.route("/comic", methods=['GET'])
def getComicList():
    headers = request.headers
    token = headers['Authorization']
    token = token[len('Bearer '):]
    if token in savedUuids:
        print('Is Authenticated User')
        return jsonify(arr)

    return jsonify(status='Failed'), 401

@app.route("/comic/<name>", methods=['DELETE'])
def deleteComic(name):
    arr.remove(name)
    return jsonify(arr)

@app.route("/comic/<name>/<page>", methods=['GET'])
def readComic(name,page):
    filename = name+'-page'+page+'.txt'
    prevfilename = getPrevPage(name, page)
    nextfilename = getNextPage(name, page)
    links = {
        'prev': prevfilename,
        'next': nextfilename
    }
    try:
        with open(filename, "r") as f:
            content = f.read()
        return jsonify(data=content, status='SUCCESS', links=links)

    except Exception as e:
        return(str(e))

if __name__ == '__main__':
    app.run(debug=True)