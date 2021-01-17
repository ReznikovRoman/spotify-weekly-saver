
import os

import spotipy
import spotipy.util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth


#####################################################################################################################


def get_discover_weekly_playlist(sp: spotipy.Spotify):
    dwp = None
    for p in sp.current_user_playlists()['items']:
        if p['name'] == 'Discover Weekly':
            dwp = sp.playlist(p['id'])

    if dwp:
        return dwp, dwp['tracks']['items'][0]['added_at']
    else:
        raise ValueError("Couldn't find ' Discover Weekly' Playlist.")


def create_archive_playlist(sp, user_id, playlist_name, description=None):
    playlist_names = [p['name'] for p in sp.current_user_playlists()['items']]

    if playlist_name not in playlist_names:
        # create new playlist
        new_dwp = sp.user_playlist_create(user_id, playlist_name, description)
        return new_dwp
    else:
        raise ValueError('Discover Weekly playlist is already archived.')


def main():
    scope = "user-read-recently-played playlist-modify-public playlist-modify-private user-read-currently-playing user-library-modify playlist-read-private user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('SPOTIFY_WEEKLY_SAVER_CLIENT_ID'),
                                                   client_secret=os.environ.get('SPOTIFY_WEEKLY_SAVER_CLIENT_SECRET'),
                                                   redirect_uri="http://localhost:8000/",
                                                   scope=scope))
    user_id = sp.me()['id']

    # get Discover Weekly playlist and its creation date
    dwp, created_at = get_discover_weekly_playlist(sp)

    # create new dwp name
    new_dwp_name = f"{dwp['name']} - {created_at.split('T')[0]}"

    # get tracks from the main dwp
    print('Getting tracks from your Discover Weekly Playlist...')
    tracks = [t['track']['id'] for t in dwp['tracks']['items']]

    # create new playlist
    print('Creating new playlist...')
    new_dwp = create_archive_playlist(sp, user_id, new_dwp_name)

    # add tracks from the main dwp to the new one
    print('Saving tracks...')
    sp.playlist_add_items(new_dwp['id'], items=tracks)


if __name__ == '__main__':
    main()
    print('Done!')













