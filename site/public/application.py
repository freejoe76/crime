from flask import Flask, render_template, url_for, redirect, abort
from flask_flatpages import FlatPages
from datetime import datetime
import pymongo
from pymongo import MongoClient
import dicts
app = Flask(__name__)
app.config.from_envvar('DENVERCRIME_SETTINGS')
client = MongoClient()
pages = FlatPages(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about/')
def flatpage():
    page = pages.get_or_404('about')
    template = page.meta.get('template', 'flatpage.html')
    return render_template(template, page=page)

def rankings_filter(neighborhood, rankings):
    # Take a neighborhood list and return a sampling of that ranking,
    # pertinent to that neighborhood.
    # We:
    #   1. Figure out where the neighborhood is in the rankings
    #   2. Make a decision about which ranking items we publish based on that.
    #print dir(rankings[0].values()[1])
    return rankings

@app.route('/neighborhood/')
def neighborhood_index():
    neighborhoods = dicts.neighborhood_lookup
    return render_template('neighborhood_index.html', neighborhoods=neighborhoods, response=None)

@app.route('/neighborhood/<neighborhood>/<about>/')
@app.route('/neighborhood/<neighborhood>/')
def neighborhood(neighborhood, about=None):
    if neighborhood not in dicts.neighborhood_lookup.keys():
        abort(404)
    neighborhood_long = dicts.neighborhood_lookup[neighborhood]
    if about == 'about':
        return render_template('neighborhood_about.html', neighborhood=neighborhood_long)
    db = client['crimedenver']
    collection_name = '%s-%s' % (neighborhood, 'timestamp')
    timestamp = db[collection_name]
    collection_name = '%s-%s' % (neighborhood, 'ticker')
    ticker = db[collection_name]
    collection_name = '%s-%s' % (neighborhood, 'recent')
    recent = db[collection_name]
    collection_name = '%s-violent' % ('rankings')
    rankings = db[collection_name]
    collection_name = '%s-property' % ('rankings')
    rankings_property = db[collection_name]
    #print rankings.find()
    response = {
       'timestamp':timestamp.find_one(),
       'ticker':ticker.find_one(),
       'recent':recent.find(),
       'rankings': {
            'violent': rankings_filter(neighborhood, rankings.find()),
            'property': rankings_property.find()
        }
    }
    if app.config.get('IN_DEV'):
        return render_template('neighborhood.html', neighborhood=neighborhood_long, response=response, in_dev=True)
    return render_template('neighborhood.html', neighborhood=neighborhood_long, response=response)

@app.route('/<shortcut>/')
def shortcut(shortcut):
    # Hard-coded shortcuts
    sc = { 'blog': 'http://blog.denvercrimes.com' }
    if shortcut in sc:
        return redirect(sc[shortcut])

    # Neighborhood shortcuts
    if shortcut in dicts.neighborhood_shortcut_lookup.keys():
        neighborhood = dicts.neighborhood_shortcut_lookup[shortcut]
        return redirect(url_for('neighborhood', neighborhood=neighborhood))
    abort(404)

#url_for('static', filename='css/style.css')


# Custom filters
@app.template_filter(name='offense')
def offense_filter(value):
    try:
        return dicts.crime_name_lookup[value].title()
    except:
        return value.replace('-', ' ').title()
app.add_template_filter(offense_filter)

@app.template_filter(name='address')
def address_filter(value):
    return value.title()
app.add_template_filter(address_filter)

@app.template_filter(name='datetime_raw')
def datetime_raw_filter(value):
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
app.add_template_filter(datetime_raw_filter)


@app.template_filter(name='datetime')
def datetime_filter(value, format='medium'):
    #print value
    if format == 'full':
        format = "%A %B %d, %I:%M %p"
    elif format == 'medium':
        format = "%A, %I:%M %p"
    try:
        return value.strftime(format)
    except:
        return None
app.add_template_filter(datetime_filter)

if __name__ == '__main__':
    app.run()
