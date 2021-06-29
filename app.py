from flask import Flask, send_file

app = Flask(__name__)

@app.route("/<id>")
def hello(id):
    # return "Hello World" + id
    filename = id + '.jpeg'
    try:
        return send_file(
            filename,
            as_attachment=True,
        )
    except FileNotFoundError as e:
        return(str(e))

if __name__ == '__main__':
    app.run(debug=True)