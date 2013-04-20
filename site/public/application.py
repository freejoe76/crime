from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/neighborhood/')
def neighborhood_index():
    return 'hi'

url_for('static', filename='css/style.css')

if __name__ == '__main__':
    app.debug = True
    app.run()
