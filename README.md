# Spotify Weekly Saver
Archives your `Discover Weekly` playlists

### Links
- [Spotipy documentation](https://github.com/plamere/spotipy)
- [Spotify developer dashboard](https://developer.spotify.com/dashboard/applications)

### Environment variables:
```
SPOTIFY_WEEKLY_SAVER_CLIENT_ID="<spotify-app-client-id>"
SPOTIFY_WEEKLY_SAVER_CLIENT_SECRET="<spotify-app-secret>"
```

### Makefile commands:
```shell
# Generate requirements.*.txt files
make compile-requirements

# Sync requirements.`example`.txt environment with the requirements.txt
make sync-requirements
```

### Startup Script
Create run.sh file (reference: [run.example.sh](run.example.sh))
