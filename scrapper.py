import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import argparse


class trackExtractor(spotipy):
    def __init__(self, user):
        self.user = user

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
            track = tracks_in_playlist(sp, user, playlist['id'])
            songs.extend(track)
        tracks = []
        songs = filter(None, songs)
        for s in songs:
            if s is not None and s['track'] is not None:
                tracks.append({'id': s['track']['id'], 'artists': s['track']
                               ['artists'], 'name': s['track']['name']})

        song_ids = set()
        for t in tracks:
            song_ids.add(t['id'])

        ret_tracks = []
        ret_tracks_string = []
        for sid in song_ids:
            for t in tracks:
                if sid == t['id']:
                    ret_tracks.append(t)
                    arts = []
                    for a in t['artists']:
                        arts.append(a['name'])
                    artists = ', '.join(arts)
                    name = t['name']
                    song = artists + '---' + name
                    ret_tracks_string.append(song)
                    break

        return songs, tracks, ret_tracks, ret_tracks_string

    def saved_tracks(sp, user):
        songs = []
        for i in range(0, 2000, 20):
            songs.extend(sp.current_user_saved_tracks(20, i)['items'])
        return songs

    def all_tracks(sp, user):
        song_ids = set()
        # saved_songs = saved_tracks(sp, user)
        # song_ids.add(i['track']['id'] for i in saved_songs)
        # for i in saved_songs:
        #    song_ids.add(i['track']['id'])

        all_songs_in_playlist, tracks = tracks_in_all_playlists(sp, user)
        for i in all_songs_in_playlist:
            song_ids.add(i['track']['id'])

        return song_ids

    def main():
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
            # print("Logged in as: " + current_user_id + '\n')
            print('Song name extracting started!')
            songs, tracks, ret_tracks, ret_tracks_string = tracks_in_all_playlists(
                sp, current_user_id)

            print(str(len(ret_tracks_string)) + ' songs extracted!')

            print('Writing songs to file!')
            tracks_as_str_file = open('tracks.txt', 'w')
            ids_file = open('ids.txt', 'w')

            for t in ret_tracks_string:
                tracks_as_str_file.write(str(t) + '\n')
            print('Songs written to file!')

            print('Writing ids to file!')

            for ids in ret_tracks:
                ids_file.write(str(ids) + '\n')

            print('Ids written to file!')
        else:
            print("Can't get token for", username)


if __name__ == "__main__":
    main()
