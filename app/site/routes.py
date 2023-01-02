from flask import (render_template, redirect, url_for)
from flask_login import login_required, current_user
import urllib.request, urllib.parse, json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from . import site
from ..auth.models import Song
from ..auth.forms import SongForm

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/song-tracks/<artist_name>')
def songTracks(artist_name):
    client_id = 'e43992d0447145cbb3f50e580d7126cf'
    client_secret = 'da0aab427ff24a4aabce560937ad3a0b'
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
    results = sp.search(q=artist_name, limit=20, type='artist')
    artist_id = results['artists']['items'][0]['id']
    tracks = sp.artist_top_tracks(artist_id=artist_id)
    return render_template('song_tracks.html', tracks=tracks['tracks'], artist_name=artist_name)

@site.route('/profile')
@login_required
def profile():
    songs = Song.get_by_user_id(current_user.id)
    return render_template('profile.html', songs=songs)

@site.route('/song/<id>/edit', methods=["GET", "POST"])
@login_required
def songEdit(id):
    song = Song.get_by_id(id)
    form = SongForm(obj=song)
    error = None
    if form.validate_on_submit():
        song.name = form.name.data
        song.guitar = form.guitar.data
        song.amp = form.amp.data
        song.pedals = form.pedals.data
        song.style = form.style.data
        song.groove = form.groove.data
        song.save()
        return redirect(url_for('site.profile'))
    return render_template('song_form.html', form=form, error=error)

@site.route('/song/add', methods=["GET", "POST"])
@login_required
def songAdd():
    song = Song()
    form = SongForm(obj=song)
    error = None
    if form.validate_on_submit():
        song.user = current_user
        song.name = form.name.data
        song.guitar = form.guitar.data
        song.amp = form.amp.data
        song.pedals = form.pedals.data
        song.style = form.style.data
        song.groove = form.groove.data
        song.save()
        return redirect(url_for('site.profile'))
    return render_template('song_form.html', form=form, error=error)

@site.route('/song/<id>/remove', methods=["GET", "POST"])
@login_required
def songRemove(id):
    song = Song.get_by_id(id)
    song.delete()
    return redirect(url_for('site.profile'))