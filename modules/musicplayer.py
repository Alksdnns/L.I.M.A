import pywhatkit
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class MusicPlayer:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="4bb973cdac58492c924b5c420c17fac4",
            client_secret="96281d24e9884a01b0be8926d493a28b",
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="user-read-playback-state user-modify-playback-state streaming"
        ))

    def play_on_spotify(self, song_name: str):
        results = self.sp.search(q=song_name, type='track', limit=1)
        if results["tracks"]["items"]:
            track_uri = results["tracks"]["items"][0]["uri"]
            self.sp.start_playback(uris=[track_uri])
            print(f"[🎧 Spotify] Playing '{song_name}'")
        else:
            print("[⚠️ Spotify] Song not found.")

    def play_on_youtube(self, song_name: str):
        pywhatkit.playonyt(song_name)
        print(f"[📺 YouTube] Playing '{song_name}'")
