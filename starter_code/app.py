# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_api import status
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.exc import SQLAlchemyError
from repository import db, Artist, Venue, Show
from forms import *
from sqlalchemy import exc
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand



# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db) 
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime



# ----------------------------------------------------------------------------#
# service
# ----------------------------------------------------------------------------#

def find_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if not venue:
       abort(404)
    else:
        return venue

def getAllVenues():
    venues = Venue.query.all()
    if not venues:  
        abort(404)
    else:
        return venues

def getAllVenuesBasedOnAreas():
     venues = getAllVenues();
     data = []
     for location in getAllCitiesAndStates(venues):
        data.append({
            "city": location[0],
            "state": location[1],
            "venues": []
        })
     for element in data:
         for venue in venues:
             if venue.city == element['city'] and venue.state == element['state']:
               element['venues'].append({
               "id": venue.id,
               "name": venue.name,
               "num_upcoming_shows": getNumberOfUpcomingShowsForVenue(venue.id)
                })
     return data
         
def getAllCitiesAndStates(venues):
    city_state = set()
    for venue in venues:
        print("venue city: "+venue.city+ "venue state: "+venue.state)
        city_state.add((venue.city, venue.state))
        
    return city_state


def getNumberOfUpcomingShowsForVenue(venue_id):
    sum = 0
    shows = Show.query.filter_by(venue_id=venue_id).all()
    for show in shows:
        print(show.venue_id)
        if show.time > datetime.now():
            sum += 1
    print(sum)
    return sum


def getNumberOfPastShowsForVenue(venue_id):
    sum = 0
    shows = Show.query.filter_by(venue_id=venue_id).all()
    for show in shows:
        print(show.venue_id)
        if show.time < datetime.now():
            sum += 1
    print(sum)
    return sum


def getUpcomingShowsByVenueId(venue_id):
    upcoming_shows = []
    shows = Show.query.filter_by(venue_id=venue_id).all()
    for show in shows:
        if show.time > datetime.now():
            show = {
            "venue_id": show.venue_id,
            "venue_name": db.session.query(Venue.name).filter_by(id=show.venue_id).first()[0],
            "artist_id": show.artist_id,
            "artist_name":  db.session.query(Artist.name).filter_by(id=show.artist_id).first()[0],
            "artist_image_link": db.session.query(Artist.image_link).filter_by(id=show.artist_id).first()[0],
            "time": show.time.strftime("%m/%d/%Y, %H:%M:%S")
             }
            upcoming_shows.append(show)
    return upcoming_shows


def getPastShowsByVenueId(venue_id):
    past_shows = []
    shows = Show.query.filter_by(venue_id=venue_id).all()
    for show in shows:
        if show.time < datetime.now():
            show = {
            "venue_id": venue_id,
            "venue_name": db.session.query(Venue.name).filter_by(id=show.venue_id).first()[0],
            "artist_id": show.artist_id,
            "artist_name":  db.session.query(Artist.name).filter_by(id=show.artist_id).first()[0],
            "artist_image_link": db.session.query(Artist.image_link).filter_by(id=show.artist_id).first()[0],
            "time": show.time.strftime("%m/%d/%Y, %H:%M:%S")
             }
            past_shows.append(show)
    return past_shows


def find_artist(aritist_id):
    artist = Artist.query.get(aritist_id)
    if not artist:
        abort(404)
    else:
        return artist

def getAllArtists():
    artists = Artist.query.all();
    if not artists:  
        abort(404)
    else:
        return artists

def getAllShows():
    shows = Show.query.all()
    data = []
    if not shows:  
        abort(404)
    else:
        for show in shows:
            show = {
            "venue_id": show.venue_id,
            "venue_name": db.session.query(Venue.name).filter_by(id=show.venue_id).first()[0],
            "artist_id": show.artist_id,
            "artist_name":  db.session.query(Artist.name).filter_by(id=show.artist_id).first()[0],
            "artist_image_link": db.session.query(Artist.image_link).filter_by(id=show.artist_id).first()[0],
            "time": show.time.strftime("%m/%d/%Y, %H:%M:%S")
             }
        data.append(show)
    return data

def getAllShowsBasedOnVenue(venue_id):
     return Show.query.filter_by(venue_id=venue_id).all()
     

def createShow(aritist_id,venue_id,time):
    artist = Artist.query.get(aritist_id)
    venue = Venue.query.get(venue_id)

    if not artist and venue:
        raise Exception("Artist or Venue id is not correct")
    else:
        return Show(
            artist_id=aritist_id,
            venue_id=venue_id,
            time=time,
        )

def showVenueService(venue_id):
    venue= find_venue(venue_id)
    return {
            "id": venue.id,
            "name": venue.name,
            "city": venue.city,
            "state": venue.state,
            "address": venue.address,
            "phone": venue.phone,
            "email": venue.email,
            "website":venue.website,
            "genres": venue.genres,
            "image_link": venue.image_link,
            "facebook_link": venue.facebook_link,
            "seeking_talent":  venue.seeking_talent,
            "description": venue.description,
            "past_shows": getPastShowsByVenueId(venue.id),
            "upcoming_shows": getUpcomingShowsByVenueId(venue.id),
            "past_shows_count":getNumberOfPastShowsForVenue(venue.id),
            "upcoming_shows_count": getNumberOfUpcomingShowsForVenue(venue.id)
    }



# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    return render_template('pages/venues.html', areas=getAllVenuesBasedOnAreas()), status.HTTP_200_OK


@app.route('/venues/search', methods=['POST'])
def search_venues():
    name = request.form.get('name', '')
    search = "%{}%".format(name)
    venue_list = Venue.query.filter(Venue.name.like(search)).all()
    result = {
        "count": len(venue_list),
        "data": venue_list
    }

    return render_template('pages/search_venues.html', results=result,
                           search_term=request.form.get('search_term', '')), status.HTTP_200_OK


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    return render_template('pages/show_venue.html', venue= showVenueService(venue_id))


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  try:
    venue = Venue(
    name = request.form.get('name', ''),
    city = request.form.get('city', ''),
    state = request.form.get('state', ''),
    address = request.form.get('address', ''),
    phone = request.form.get('phone', ''),
    email = request.form.get('email', ''),
    website =  request.form.get('website', ''),
    genres = request.form.getlist('genres'),
    image_link = request.form.get('image_link', ''),
    facebook_link = request.form.get('facebook_link', ''),
    seeking_talent = request.form.get('seeking_talent',''),
    description = request.form.get('description','')
    )
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue was successfully listed!')
    return render_template('pages/home.html'), status.HTTP_201_CREATED
  except Exception as e:
    flash(f'An error occurred. venue could not be listed. Error: {e}')
    db.session.rollback()
    return render_template('forms/new_venue.html', form=form)
  finally:
    db.session.close()


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue = find_venue(venue_id)
        shows = getAllShowsBasedOnVenue(venue_id)

        if shows:
            for show in shows:
                db.session.delete(show)

        db.session.delete(venue)
        flash('Venue was successfully deleted!')
        db.session.commit()
        return  status.HTTP_200_OK
    except Exception as e:
        print(e)
        flash(f'An error occurred. venue could not be listed. Error: {e}')
        db.session.rollback()
        return render_template('pages/show_venue.html', venue= showVenueService(venue_id))
    finally:
       db.session.close()



      

 #  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    
    return render_template('pages/artists.html', artists=getAllArtists()),status.HTTP_200_OK



@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = find_artist(artist_id)
    # artistShows = getArtistShows(artist_id)
    return render_template('pages/show_artist.html', artist=artist
    # shows = artistShows
    )


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = find_artist(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        artist = find_artist(artist_id)
        artist.name =  request.form.get('name')
        artist.city =  request.form.get('city')
        artist.state = request.form.get("state"),
        artist.address = request.form.get("address"),
        artist.phone = request.form.get("phone"),
        artist.genres = request.form.getlist("genres"),
        artist.image_link = request.form.get("img_link"),
        artist.facebook_link = request.form.get("facebook_link"),
        artist.website = request.form.get("website"),
        artist.seeking_venue = request.form.get("seeking_venue"),
        artist.description = request.form.get("description")
        db.session.commit()
        flash('Artist was successfully updated!')
        return redirect(url_for('show_artist', artist_id=artist_id))
    except Exception as e:
        flash(f'An error occurred: {e}')
        db.session.rollback()
        return render_template('forms/edit_artist.html',artist=artist, form=form)
    finally:
        db.session.close()

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = find_venue(venue_id)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  try:
    venue = find_venue(venue_id)
    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.address = request.form.get('address')
    venue.phone = request.form.get('phone')
    venue.email = request.form.get('email')
    venue.website =  request.form.get('website')
    venue.genres = request.form.getlist('genres')
    venue.image_link = request.form.get('image_link')
    facebook_link = request.form.get('facebook_link')
    seeking_talent = request.form.get('seeking_talent')
    description = request.form.get('description')
    db.session.commit()
    flash('Venue with name: '+venue.name+' was successfully updayed!')
    return redirect(url_for('show_venue', venue_id=venue_id)),status.HTTP_202_ACCEPTED
  except Exception as e:
    flash(f'An error occurred: {e}')
    db.session.rollback()
    return render_template('forms/edit_venue.html', form=form)
  finally:
    db.session.close()  
    


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    try:
        artist = Artist(
            name = request.form.get("name"),
            city = request.form.get("city"),
            state = request.form.get("state"),
            address = request.form.get("address"),
            phone = request.form.get("phone"),
            genres = request.form.getlist("genres"),
            image_link = request.form.get("img_link"),
            facebook_link = request.form.get("facebook_link"),
            website = request.form.get("website"),
            seeking_venue = request.form.get("seeking_venue"),
            description = request.form.get("description")
    )
        db.session.add(artist)
        db.session.commit()
        flash('Artist was successfully listed!')
        return render_template('pages/home.html'), status.HTTP_201_CREATED
    except Exception as e:
        flash(f'An error occurred. Show could not be listed. Error: {e}')
        db.session.rollback()
        return render_template('forms/new_artist.html', form=form)
    finally:
        db.session.close()
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    return render_template('pages/shows.html', shows=getAllShows())


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm()
    try:
        show = createShow(request.form.get('artist_id'),
        request.form.get('venue_id'),request.form.get('time'))
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
        return render_template('pages/home.html'), status.HTTP_201_CREATED
    except Exception as e:
        flash(f'An error occurred: {e}')
        db.session.rollback()
        return render_template('forms/new_show.html', form=form)
    finally:
        db.session.close()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
