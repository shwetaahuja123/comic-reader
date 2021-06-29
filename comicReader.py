from flask import Flask, jsonify, send_file, request
from utilities import getPrevPage, getNextPage
from init import users
import uuid
from loggerMiddleware import LoggerMiddleware, savedUuids
# from flask_restful import Api

# print('here', i)
app = Flask(__name__)
arr = ['Tom And Jerry', 'Lion King']

app.wsgi_app = LoggerMiddleware(app.wsgi_app)


@app.route("/login", methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    if(email in users and password == users[email]):
        msg = 'User authenticated'
        generated_uuid = uuid.uuid4()

        savedUuids[str(generated_uuid)] = email
        print('savedUuids: ', savedUuids)
        return jsonify(data=msg, uuid=generated_uuid)
    else:
        msg = 'Invalid user'
        return jsonify(data=msg)

@app.route("/comic", methods=['GET'])
def getComicList():
    headers = request.headers
    token = headers['Authorization']
    token = token[len('Bearer '):]
    print(token)
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
        # print(content)
        return jsonify(data=content, status='SUCCESS', links=links)
    # return send_file(
    #         filename,
    #         as_attachment=True,
    #     )
    except Exception as e:
        return(str(e))

if __name__ == '__main__':
    app.run(debug=True)