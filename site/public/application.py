from flask import Flask, render_template, url_for
import dicts
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/neighborhood/')
@app.route('/neighborhood/<neighborhood>/')
def neighborhood(neighborhood=None):
    return render_template('neighborhood.html', neighborhood=neighborhood)

@app.route('/<shortcut>/')
def shortcut(shortcut):
    return render_template('neighborhood.html', neighborhood=neighborhood)

#url_for('static', filename='css/style.css')

if __name__ == '__main__':
    app.debug = True
    app.run()
