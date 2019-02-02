import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import argparse


def all_playlists(sp, user):
    playlists = []
    for i in range(0, 1000, 50):
        playlists.extend(sp.user_playlists(user, 50, i)['items'])

    return playlists


def tracks_in_playlist(sp, user, playlist):
    return sp.user_playlist_tracks(user, playlist)['items']


def tracks_in_all_playlists(sp, user):
    playlists = all_playlists(sp, user)
    songs = []
    for playlist in playlists:
        songs.extend(tracks_in_playlist(
            sp, user, playlist['uri'].split(':')[-1]))
    return songs


def saved_tracks(sp, user):
    songs = []
    for i in range(0, 2000, 20):
        songs.extend(sp.user_saved_tracks(user, 20, i))
    return songs


def all_tracks(sp, user):
    all_songs = list(set(tracks_in_all_playlists(
        sp, user) + saved_tracks(sp, user)))
    return all_songs


def main(args):
    username = 'shaquzum'
    scope = 'user-library-read playlist-read-private playlist-modify-private playlist-modify-public user-top-read user-read-recently-played'
    cid = 'eaceec9fa2be44368ac074498a7c7b2b'
    secret = 'baf792989764463fa4f674eafff8edc1'
    redirect_uri = 'http://localhost:8888/callback/'
    # artist_to_discover_uri = '0HgZEgGO4KjuGbeAXXl25w'
    SpotifyClientCredentials(client_id=cid, client_secret=secret)
    token = util.prompt_for_user_token(
        username, scope, redirect_uri=redirect_uri)

    if token:
        sp = spotipy.Spotify(auth=token)
        current_user_id = sp.current_user()['id']
        print("Logged in as: " + current_user_id + '\n')

        print(all_tracks(sp, current_user_id))

        '''
                break
        print(saved_songs)
        playlist_songs = [sp.user_playlist_tracks(
            current_user_id, plid, 1000) for plid in playlists]
        songs = set(saved_songs + playlist_songs)
        print(songs)
        '''
    else:
        print("Can't get token for", username)


if __name__ == "__main__":
    args = None
    main(args)
