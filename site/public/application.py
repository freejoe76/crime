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
    #recent.create_index('_FIRST_OCCURRENCE_DATE')
    collection_name = '%s-violent' % ('rankings')
    rankings = db[collection_name]
    collection_name = '%s-property' % ('rankings')
    rankings_property = db[collection_name]
    print recent.find().sort("_LAST_OCCURRENCE_DATE", 1)[0]
    # { orderby: { 'OFFENSE_CODE', 1 } } )
    response = {
       'timestamp':timestamp.find_one(),
       'ticker':ticker.find_one(),
       'recent':recent.find().sort('_FIRST_OCCURRENCE_DATE', 1),
       'rankings': {
            'violent': rankings.find(),
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
    print value
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
