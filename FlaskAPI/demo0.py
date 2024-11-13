from flask import Flask

app = Flask(__name__)

@app.route("/")
def helloworld():
    return 'hello Flask'
@app.route('/test/<name>')
def greet(name):
    return f'hello {name}'
if __name__ == "__main__":
    app.run(debug=True)