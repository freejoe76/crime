from flask import Flask, render_template, url_for, redirect, abort
from datetime import datetime
import pymongo
from pymongo import MongoClient
import dicts
app = Flask(__name__)
client = MongoClient()


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('flatpage.html', page='about')

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
    return render_template('neighborhood.html', neighborhood=neighborhood)
@app.route('/neighborhood/<neighborhood>/')
def neighborhood(neighborhood):
    if neighborhood not in dicts.neighborhood_lookup.keys():
        abort(404)
    neighborhood_long = dicts.neighborhood_lookup[neighborhood]
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
    print rankings.find()
    response = {
       'timestamp':timestamp.find_one(),
       'ticker':ticker.find_one(),
       'recent':recent.find(),
       'rankings': {
            'violent': rankings_filter(neighborhood, rankings.find()),
            'property': rankings_property.find()
        }
    }
    return render_template('neighborhood.html', neighborhood=neighborhood_long, response=response)

@app.route('/<shortcut>/')
def shortcut(shortcut):
    if shortcut in dicts.neighborhood_shortcut_lookup.keys():
        neighborhood = dicts.neighborhood_shortcut_lookup[shortcut]
        return redirect(url_for('neighborhood', neighborhood=neighborhood))
    abort(404)

#url_for('static', filename='css/style.css')


# Custom filters
@app.template_filter(name='offense')
def offense_filter(value):
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
    return value.strftime(format)
app.add_template_filter(datetime_filter)

if __name__ == '__main__':
    app.debug = True
    app.run()
