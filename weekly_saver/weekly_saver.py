import os
from typing import Tuple

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


def get_discover_weekly_playlist(spotify_instance: Spotify) -> Tuple[dict, str]:
    dwp = None
    for playlist in spotify_instance.current_user_playlists()['items']:
        if playlist['name'] == 'Discover Weekly':
            dwp = spotify_instance.playlist(playlist['id'])

    if dwp:
        return dwp, dwp['tracks']['items'][0]['added_at']
    raise ValueError("Error: Couldn't find Discover Weekly Playlist.")


def is_already_archived(playlist_name: str) -> bool:
    with open('archived_playlists.txt', 'r') as f:
        content = f.read()
    return playlist_name in content


def archive_discover_weekly_playlist(
        spotify_instance: Spotify,
        user_id: str,
        playlist_name: str,
        description: str = None,
) -> dict:
    if is_already_archived(playlist_name):
        raise ValueError("Error: Discover Weekly playlist is already archived.")

    new_dwp = spotify_instance.user_playlist_create(user_id, playlist_name, description)

    with open('archived_playlists.txt', 'w') as f:
        f.write(playlist_name)

    return new_dwp


def main() -> None:
    with open('archived_playlists.txt', 'a+'):
        pass

    scope = "user-read-recently-played " \
            "playlist-modify-public " \
            "playlist-modify-private " \
            "user-read-currently-playing " \
            "user-library-modify " \
            "playlist-read-private " \
            "user-library-read"
    spotify_credentials = SpotifyOAuth(
        client_id=os.environ.get('SPOTIFY_WEEKLY_SAVER_CLIENT_ID'),
        client_secret=os.environ.get('SPOTIFY_WEEKLY_SAVER_CLIENT_SECRET'),
        redirect_uri="http://localhost:8000/",
        scope=scope,
    )
    spotify_instance = Spotify(auth_manager=spotify_credentials)
    user_id = spotify_instance.me().get('id')

    # get Discover Weekly playlist and its creation date
    dwp, created_at = get_discover_weekly_playlist(spotify_instance)

    # create new dwp name
    new_dwp_name = f"{dwp['name']} - {created_at.split('T')[0]}"

    # get tracks from the main dwp
    print('Getting tracks from your Discover Weekly Playlist...')
    tracks = [t['track']['id'] for t in dwp['tracks']['items']]

    # create new playlist
    print('Creating new playlist...')
    new_dwp = archive_discover_weekly_playlist(spotify_instance, user_id, new_dwp_name)

    # add tracks from the main dwp to the new one
    print('Saving tracks...')
    spotify_instance.playlist_add_items(new_dwp['id'], items=tracks)


if __name__ == '__main__':
    try:
        main()
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)
    else:
        print('Done!')
