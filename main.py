import argparse
from spoti import TrackExtractor
from scrapper import Scrapper


def parse_arguments():
    parser = argparse.ArgumentParser(description="Main script")
    parser.add_argument('-u', '--username', default='shaquzum',
                        help="Username of the user.")
    parser.add_argument('-c', '--cid', default='eaceec9fa2be44368ac074498a7c7b2b',
                        help="Client id.")
    parser.add_argument('-s', '--secret', default='baf792989764463fa4f674eafff8edc1',
                        help="Secret code after creation of app in spotify developer page.")
    parser.add_argument("-r", "--redirect_uri", default='http://localhost:8888/callback/',
                        help="Redirect uri got after creation of app.")
    parser.add_argument("-d", "--content", choices=['all', 'playlists', 'saved_tracks'],
                        default='all', help="Which part of library to be scrapped.")
    args = parser.parse_args()
    return args


def main(args):
    username = args.username
    cid = args.cid
    secret = args.secret
    redirect_uri = args.redirect_uri
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

    for s in ret_tracks:
        for a in s['track']['artists']:
            lyrics = sc.lyrics_extractor(s['name'], s['track']['name'])
            if lyrics != '404':
                f = open((','.join(x['name']
                                   for x in a) + s['track']['name']), 'w+')
                f.write(lyrics)
                f.close()
            else:
                print('Lyrics for ' + (','.join(x['name']
                                                for x in a) + s['track']['name']) + ' could not be found!')


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
