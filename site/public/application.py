from flask import Flask, render_template, url_for, redirect, abort
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
    if shortcut in dicts.neighborhood_shortcut_lookup.keys():
        neighborhood = dicts.neighborhood_shortcut_lookup[shortcut]
        return redirect(url_for('neighborhood', neighborhood=neighborhood))
    abort(404)

#url_for('static', filename='css/style.css')

if __name__ == '__main__':
    app.debug = True
    app.run()
