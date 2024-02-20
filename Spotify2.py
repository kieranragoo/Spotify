import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()

CLIENT_ID = os.getenv("client_id")
CLIENT_SECRET = os.getenv("client_secret")


class Playlist:

    def __init__(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(scope="user-library-read playlist-modify-private user-library-read user-top-read playlist-read-private playlist-read-collaborative",
                                      redirect_uri="https://k_ragoo.com/callback",
                                      client_id=CLIENT_ID,
                                      client_secret=CLIENT_SECRET,
                                      show_dialog=True,
                                      cache_path="token.txt"))
        self.total = self.get_total()
        self.uris = []
        self.url = ''
        self.playlist_id = ''

    def get_total(self):
        results = self.sp.current_user_saved_tracks(limit=1)
        total = results['total']
        print('You have {} liked songs.'.format(total))
        return total

    def get_all_songs(self):
        total_retrieved = 0
        while total_retrieved < self.total and total_retrieved < 50:
            results = self.sp.current_user_saved_tracks(
                limit=50, offset=total_retrieved)
            for item in results['items']:
                track = item['track']
                self.uris.append(track['uri'])
                total_retrieved += 1

    def get_playlist_id(self):

        playlist_id = self.sp.user_playlists(1116784764)
        for item in playlist_id['items']:
            if item['name'] == 'Liked songs 50':
                id = item['uri']

                tracks = []

                for track in self.sp.playlist_tracks(id)["items"]:
                    track_uri = track["track"]["uri"]
                    result = track_uri
                    tracks.append(result)

                self.sp.user_playlist_remove_all_occurrences_of_tracks(
                    1116784764, id, tracks, snapshot_id=None)

        return id

    def populate_playlist(self, id):
        for i in range(0, len(self.uris), 100):
            self.sp.playlist_add_items(
                playlist_id=id, items=self.uris[i:i+100])
        print('Your playlist is ready at {}'.format(self.url))


playlist = Playlist()
playlist.get_all_songs()
id = playlist.get_playlist_id()
playlist.populate_playlist(id)
