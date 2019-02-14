import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import argparse


class TrackExtractor:
    def __init__(self, username, cid, secret, redirect_uri):
        self.username = username
        self.scope = 'user-library-read playlist-read-private playlist-modify-private playlist-modify-public user-top-read user-read-recently-played'
        self.cid = cid
        self.secret = secret
        self.redirect_uri = redirect_uri
        # artist_to_discover_uri = '0HgZEgGO4KjuGbeAXXl25w'
        SpotifyClientCredentials(client_id=self.cid, client_secret=self.secret)
        token = util.prompt_for_user_token(
            self.username, self.scope, redirect_uri=self.redirect_uri)

        if token:
            self.sp = spotipy.Spotify(auth=token)
            self.current_user_id = self.sp.current_user()['id']
        else:
            print("Can't get token for", username)
            quit()

    def write_to_file(self, filename, l):
        print('Filling ' + str(filename))
        file = open(filename, 'w+')
        file.write('[\n')

        for t in l:
            file.write(str(t) + '\n')

        file.write(']\n')
        print(filename + ' filled with ' +
              str(len(l)) + ' lines!')

    def all_playlists(self):
        playlists = []
        for i in range(0, 1000, 50):
            playlists.extend(self.sp.user_playlists(
                self.current_user_id, 50, i)['items'])

        return playlists

    def tracks_in_playlist(self, playlist):
        return self.sp.user_playlist_tracks(self.current_user_id, playlist)['items']

    def tracks_in_all_playlists(self):
        playlists = self.all_playlists()
        songs = []
        for playlist in playlists:
            track = self.tracks_in_playlist(playlist['id'])
            songs.extend(track)
        song_ids_set = set()

        for s in songs:
            if s is not None and s['track'] is not None:
                song_ids_set.add(s['track']['id'])

        ret_tracks = []
        ret_tracks_string = []

        for sid in song_ids_set:
            for s in songs:
                if s['track'] is not None:
                    if sid == s['track']['id']:
                        ret_tracks.append(s)
                        song = (', '.join([a['name']
                                           for a in s['track']['artists']])) + '---' + s['track']['name']
                        ret_tracks_string.append(song)
                        break

        self.write_to_file('tracks_in_all_playlists.json', ret_tracks)
        self.write_to_file(
            'tracks_in_all_playlists_names.txt', ret_tracks_string)

        return ret_tracks, ret_tracks_string, song_ids_set

    def saved_tracks(self):
        songs = []
        for i in range(0, 2000, 20):
            songs.extend(self.sp.current_user_saved_tracks(20, i)['items'])

        song_ids_set = set()

        for s in songs:
            if s is not None and s['track'] is not None:
                song_ids_set.add(s['track']['id'])

        ret_tracks = []
        ret_tracks_string = []

        for sid in song_ids_set:
            for s in songs:
                if s['track'] is not None:
                    if sid == s['track']['id']:
                        ret_tracks.append(s)
                        song = (', '.join([a['name']
                                           for a in s['track']['artists']])) + '---' + s['track']['name']
                        ret_tracks_string.append(song)
                        break

        self.write_to_file('saved_tracks.json', ret_tracks)
        self.write_to_file('saved_tracks_names.txt', ret_tracks_string)

        return ret_tracks, ret_tracks_string, song_ids_set

    def all_tracks(self):

        ret_tracks_saved, _, song_ids_set_saved_songs = self.saved_tracks()
        ret_tracks_pl, _, song_ids_set_pl = self.tracks_in_all_playlists()
        song_ids_set = song_ids_set_saved_songs.union(song_ids_set_pl)
        all_tracks = []
        all_tracks_string = []

        ret_tracks = ret_tracks_saved + ret_tracks_pl

        for sid in song_ids_set:
            for t in ret_tracks:
                if t['track'] is not None:
                    if sid == t['track']['id']:
                        all_tracks.append(t)
                        song = (', '.join([a['name']
                                           for a in t['track']['artists']])) + '---' + t['track']['name']
                        all_tracks_string.append(song)
                        break

        self.write_to_file('all_tracks.json', all_tracks)
        self.write_to_file('all_tracks_names.txt', all_tracks_string)

        return all_tracks, all_tracks_string, song_ids_set


'''
def main():
    username = 'shaquzum'
    scope = 'user-library-read playlist-read-private playlist-modify-private playlist-modify-public user-top-read user-read-recently-played'
    cid = 'eaceec9fa2be44368ac074498a7c7b2b'
    secret = 'baf792989764463fa4f674eafff8edc1'
    redirect_uri = 'http://localhost:8888/callback/'
    # artist_to_discover_uri = '0HgZEgGO4KjuGbeAXXl25w'
    extractor = TrackExtractor(username, scope, cid, secret, redirect_uri)
    extractor.all_tracks()
    print('Finished extracting tracks!')
'''
