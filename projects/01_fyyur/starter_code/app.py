#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

# TODO: connect to a local postgresql database
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column('artist_id',db.Integer,db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column('venue_id',db.Integer,db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column('start_time', db.TIMESTAMP, nullable=False)
  venue = db.relationship("Venue",backref="Artist")
  artist = db.relationship("Artist",backref="Venue")

  def __repr__(self):
    return f'<Artist id: {self.artist_id} , venue_id: {self.venue_id}, start time: {self.start_time}>'

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String))
    website =  db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    artist = db.relationship("Show",backref="Venue")

    def __repr__(self):
      return f'<id: {self.id}, name: {self.name}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String))
    website =  db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    venues = db.relationship("Show",backref="Artist")

    def __repr__(self):
      return f'<id: {self.id} , name: {self.name}>'
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    ven = db.session.query(Venue.city,Venue.state).group_by('city','state').all()
    for city in ven:
        venueInfo = db.session.query(Venue.id,Venue.name).filter_by(city=city[0], state=city[1])
        infos = []
        for info in venueInfo:
          num = getNumUpcomingShows(info[0])  
          infos.append({'id':info[0],"name":info[1],"num_upcoming_shows":num})
        col = {"city":city[0], "state":city[1],"venues":infos}
        data.append(col)
        
    return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  term = request.form.get('search_term')
  res = db.session.query(Venue.id,Venue.name).filter(Venue.name.ilike('%'+term+'%')).all()
  data = []
  for i in res:
    num = getNumUpcomingShows(i[0])
    data.append({"id":i[0],"name":i[1],"num_upcoming_shows": num })    
  response={
    "count": len(res),
    "data":data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  _data = db.session.query(Venue).get(venue_id)
  upcoming_shows_count ,upcoming_shows = getNumUpcomingShows(venue_id,'ven', 1)
  past_shows_count ,past_shows = getNumPastShows(venue_id,'ven',1)
  data1={
    "id": _data.id,
    "name": _data.name,
    "genres": _data.genres,
    "address": _data.address,
    "city": _data.city,
    "state": _data.state,
    "phone": _data.phone,
    "website": _data.website,
    "facebook_link":_data.facebook_link,
    "seeking_talent": _data.seeking_talent,
    "seeking_description": _data.seeking_description,
    "image_link":_data.image_link,
    "past_shows":past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }
  
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data1)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  err =0
  try:
    ven = Venue(name = request.form['name'],city=request.form['city'],state=request.form['state'],
                address=request.form['address'],phone=request.form['phone'],genres=request.form.getlist('genres'),
                facebook_link=request.form['facebook_link'] )
    db.session.add(ven)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    err =1
  finally:
    db.session.close()
    
  # TODO: modify data to be the data object returned from db insertion
  if err == 0:
    name = db.session.query(Venue.name).filter_by(name=request.form['name']).order_by(db.desc(Venue.id)).first()[0]
    # on successful db insert, flash success
    flash('Venue ' + name + ' was successfully listed!')
  else:
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    db.session.query(Show).filter_by(venue_id=id).delete()
    db.session.query(Venue).filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exec_info())
    err = 1
  finally:
    db.session.close()
  
  if err == 0:
    flush('Venue Deleted Successfully')
  else:
    flush('Error!! Could not delete Venue')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = db.session.query(Artist.id,Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  term = request.form.get('search_term')
  res = db.session.query(Artist.id,Artist.name).filter(Artist.name.ilike("%"+term+"%")).all()
  _data = []
  for i in res:
    num_upcoming_shows = getNumUpcomingShows(i[0],'art')
    _data.append({"id":i[0],"name":i[1],"num_upcoming_shows": num_upcoming_shows })
  response={
    "count": len(res),
    "data":_data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  _data = db.session.query(Artist).get(artist_id)
  upcoming_shows_count ,upcoming_shows = getNumUpcomingShows(artist_id,'art', 1)
  past_shows_count ,past_shows = getNumPastShows(artist_id,'art',1)
  data={
    "id": _data.id,
    "name":_data.name,
    "genres": _data.genres,
    "city": _data.city,
    "state": _data.state,
    "phone": _data.phone,
    "website": _data.website,
    "facebook_link": _data.facebook_link,
    "seeking_venue": _data.seeking_venue,
    "seeking_description": _data.seeking_description,
    "image_link": _data.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }
  
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  artist = Artist.query.get(artist_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  form = ArtistForm(obj = artist)
  form.populate_obj(artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  err = 0
  dict = {
    "name":request.form['name'],
    "city":request.form['city'],
    "state":request.form['state'],
    "phone":request.form['phone'],
    "genres":request.form.getlist('genres'),
    "facebook_link":request.form['facebook_link'] }
  try:
    db.session.query(Artist).filter_by(id=artist_id).update(dict)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exec_info())
    err = 1
  finally:
    db.session.close()
  
  if err == 0:
    flash("Updated Successfully")
  else:
    flash("Error!! Not Updated")
              
  
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  ven = Venue.query.get(venue_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  form = VenueForm(obj = ven)
  form.populate_obj(ven)
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=ven)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  err = 0
  dict = {
    "name":request.form['name'],
    "city":request.form['city'],
    "state":request.form['state'],
    "phone":request.form['phone'],
    "genres":request.form.getlist('genres'),
    "facebook_link":request.form['facebook_link'] }
  try:
    db.session.query(Venue).filter_by(id=venue_id).update(dict)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exec_info())
    err = 1
  finally:
    db.session.close()
  
  if err == 0:
    flash("Updated Successfully")
  else:
    flash("Error!! Not Updated")

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  err =0
  art = Artist(name = request.form['name'],city=request.form['city'],state=request.form['state'],
              phone=request.form['phone'],genres=request.form.getlist('genres'),
              facebook_link=request.form['facebook_link'] )
  try:
    db.session.add(art)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    err =1
  finally:
    db.session.close()
    
  # TODO: modify data to be the data object returned from db insertion
  if err == 0:
    name = db.session.query(Artist.name).filter_by(name=request.form['name']).order_by(db.desc(Artist.id)).first()[0]
    # on successful db insert, flash success
    flash('Artist ' + name + ' was successfully listed!')
  else:
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  shows_data = db.session.query(Show).all()
  for show in shows_data:
    art = db.session.query(Artist.name,Artist.id,Artist.image_link).filter_by(id=show.artist_id).all()
    ven = db.session.query(Venue.name,Venue.id).filter_by(id=show.venue_id).all()
    data.append({
    "venue_id": ven[0][1],
    "venue_name": ven[0][0],
    "artist_id": art[0][1],
    "artist_name": art[0][0],
    "artist_image_link": art[0][2],
    "start_time": str(show.start_time)
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  sh = Show(artist_id=request.form['artist_id'],venue_id=request.form['artist_id'],
            start_time=request.form['start_time'])
  err=0
  try:
    db.session.add(sh)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    err =1
  finally:
    db.session.close()
    
  # TODO: modify data to be the data object returned from db insertion
  if err == 0:
    flash('Show was successfully listed!')
  else:
    flash('An error occurred. Show could not be listed.')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

def getNumUpcomingShows(id, idType='ven', get_data=0):
  
  if idType=='ven':
    shows = db.session.query(Show.start_time,Show.artist_id).filter_by(venue_id = id).all()
  elif idType=='art':
    shows = db.session.query(Show.start_time,Show.artist_id).filter_by(artist_id = id).all()
  
  num = 0
  cur = datetime.today()
  info = []
  for show in shows:
   
    if (show[0].date() > cur.date() ) or (show[0].date() == cur.date() and show[0].time() > cur.time() ):
      num = num +1
      if idType == 'ven':
        art = db.session.query(Artist.name,Artist.image_link).filter_by( id=show[1] ).all()
        info.append({
          "artist_id": show[1],
          "artist_name": art[0][0],
          "artist_image_link": art[0][1],
          "start_time": str(show[0])
        })
      elif idType == 'art':
        ven = db.session.query(Venue.name,Venue.image_link).filter_by( id=show[1] ).all()
        info.append({
          "venue_id": show[1],
          "venue_name": ven[0][0],
          "venue_image_link": ven[0][1],
          "start_time": str(show[0])
        })
  if get_data == 1:
    return num,info
  return num

def getNumPastShows(id, idType='ven', get_data=0):
  if idType=='ven':
    shows = db.session.query(Show.start_time,Show.artist_id).filter_by(venue_id = id).all()
  elif idType=='art':
    shows = db.session.query(Show.start_time,Show.artist_id).filter_by(artist_id = id).all()
  num = 0
  cur = datetime.today()
  info = []
  for show in shows:
    if (show[0].date() < cur.date() ) or (show[0].date() == cur.date() and show[0].time() < cur.time() ):
      num = num +1
      if idType == 'ven':
        art = db.session.query(Artist.name,Artist.image_link).filter_by( id=show[1] ).all()
        info.append({
          "artist_id": show[1],
          "artist_name": art[0][0],
          "artist_image_link": art[0][1],
          "start_time": str(show[0])
        })
      elif idType == 'art':
        ven = db.session.query(Venue.name,Venue.image_link).filter_by( id=show[1] ).all()
        info.append({
          "venue_id": show[1],
          "venue_name": ven[0][0],
          "venue_image_link": ven[0][1],
          "start_time": str(show[0])
        })
  if get_data == 1:
    return num,info
  return num

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
