from typing import List, Tuple

from spotipy import Spotify, SpotifyOAuth


class SpotifyHandler:
    """Handles Spotipy API."""

    def __init__(self, spotify_instance: Spotify):
        self._spotify_instance = spotify_instance

    def get_spotify_instance(self) -> Spotify:
        return self._spotify_instance

    def set_spotify_instance(self, spotify_instance: Spotify) -> None:
        self._spotify_instance = spotify_instance

    def refresh_access_token(self, spotify_credentials: SpotifyOAuth) -> str:
        cached_token: dict = spotify_credentials.get_cached_token()
        refreshed_token: str = cached_token.get('refresh_token')
        new_token: dict = spotify_credentials.refresh_access_token(refreshed_token)
        new_access_token = new_token.get('access_token')

        spotify_instance = Spotify(auth=new_access_token)
        self._spotify_instance = spotify_instance
        return new_access_token

    def get_current_user_playlists_data(self) -> List[dict]:
        playlists_api_limit = 50
        playlists_api_offset = 0
        user_playlists: dict = self._spotify_instance.current_user_playlists(
            limit=playlists_api_limit,
            offset=playlists_api_offset,
        )
        playlists_total: int = user_playlists.get('total')
        playlists_api_calls_count = round(playlists_total / playlists_api_limit)
        playlist_names = [playlist for playlist in user_playlists.get('items')]

        while playlists_api_calls_count:
            playlists_api_offset += playlists_api_limit
            user_playlists: dict = self._spotify_instance.current_user_playlists(
                limit=playlists_api_limit,
                offset=playlists_api_offset,
            )
            playlist_names.extend([playlist for playlist in user_playlists.get('items')])
            playlists_api_calls_count -= 1
        return playlist_names

    def get_discover_weekly_playlist(self) -> Tuple[dict, str]:
        dwp = None
        current_user_playlists = self.get_current_user_playlists_data()
        for playlist_data in current_user_playlists:
            if playlist_data.get('name') == 'Discover Weekly':
                dwp = self._spotify_instance.playlist(playlist_data.get('id'))

        if dwp:
            return dwp, dwp['tracks']['items'][0]['added_at']
        raise ValueError("Error: Couldn't find Discover Weekly Playlist.")

    def is_discover_weekly_playlist_already_in_spotify(self, playlist_name: str) -> bool:
        playlist_names: List[str] = [
            playlist_data.get('name')
            for playlist_data in self.get_current_user_playlists_data()
        ]
        return playlist_name in playlist_names
