from typing import Tuple, Dict

from spotipy import Spotify, SpotifyOAuth

from constants import DISCOVER_WEEKLY_PLAYLIST_NAME


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

    def get_current_user_playlists_data(self) -> Dict[str, dict]:
        playlists_api_limit = 50
        playlists_api_offset = 0
        user_playlists: dict = self._spotify_instance.current_user_playlists(
            limit=playlists_api_limit,
            offset=playlists_api_offset,
        )
        playlists_total: int = user_playlists.get('total')
        playlists_api_calls_count = round(playlists_total / playlists_api_limit)
        playlist_data = {
            playlist.get('name'): playlist
            for playlist in user_playlists.get('items')
        }

        while playlists_api_calls_count:
            playlists_api_offset += playlists_api_limit
            user_playlists: dict = self._spotify_instance.current_user_playlists(
                limit=playlists_api_limit,
                offset=playlists_api_offset,
            )
            playlist_data.update({playlist.get('name'): playlist for playlist in user_playlists.get('items')})
            playlists_api_calls_count -= 1
        return playlist_data

    def get_discover_weekly_playlist(self) -> Tuple[dict, str]:
        dwp = self.get_current_user_playlists_data().get(DISCOVER_WEEKLY_PLAYLIST_NAME)
        if dwp is None:
            raise ValueError(f"Error: Couldn't find {DISCOVER_WEEKLY_PLAYLIST_NAME} Playlist.")

        dwp_spotify = self._spotify_instance.playlist(dwp.get('id'))
        return dwp_spotify, dwp_spotify['tracks']['items'][0]['added_at']

    def is_discover_weekly_playlist_already_in_spotify(self, playlist_name: str) -> bool:
        return playlist_name in self.get_current_user_playlists_data().keys()
