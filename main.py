import argparse
from spoti import TrackExtractor
from scrapper import Scrapper
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description="Main script")
    parser.add_argument('-u', '--username', default='shaquzum',
                        help="Username of the user.")
    parser.add_argument("-d", "--content", choices=['all', 'playlists', 'saved_tracks'],
                        default='all', help="Which part of library to be scrapped.")
    args = parser.parse_args()
    return args


def main(args):
    username = args.username
    cid = os.environ['SPOTIPY_CLIENT_ID']
    secret = os.environ['SPOTIPY_CLIENT_SECRET']
    redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']
    content = args.content

    spoti = TrackExtractor(username, cid, secret, redirect_uri)
    sc = Scrapper()
    if content == 'all':
        ret_tracks, _, _ = spoti.all_tracks()
    elif content == 'playlists':
        ret_tracks, _, _ = spoti.tracks_in_all_playlists()
    elif content == 'saved_tracks':
        ret_tracks, _, _ = spoti.saved_tracks()
    else:
        print(
            'Wrong set of filter! Please enter one of [\'all\', \'playlists\',\'saved_tracks\']')

    

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
