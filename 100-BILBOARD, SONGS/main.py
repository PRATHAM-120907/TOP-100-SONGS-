import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import requests
from bs4 import BeautifulSoup

client_id = "YOUR CLIENT ID"
client_secret = "YOUR CLIENT SECRET" 


date = input("ENTER THE TIME PERIOD OF WHICH YOU NEED THE TOP SONGS IN  YYYY-MM-DD FORMAT :")

url = f"https://www.billboard.com/charts/hot-100/{date}/"

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}


response = requests.get(url=url, headers=header)

soup = BeautifulSoup(response.text ,"html.parser")


song_names_span  = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_span]



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
print(user_id)


songs_uris = []
year= date.split("-")[0]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}" , type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id ,name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uris)


