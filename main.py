import requests
import spotipy
from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
load_dotenv()
date=input("Which year do you want to travel to? Type the date in this format yyyy-mm-dd ")
year=date.split("-")[0]

html = requests.get(f"https://www.billboard.com/charts/hot-100/{date}").text
soup=BeautifulSoup(html,"html.parser")
song_names_spans = soup.select("li ul li h3")

song_names_list=[song_name.getText().strip() for song_name in song_names_spans]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    redirect_uri="https://www.west.com",
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path="token.txt",

)
)
spotify_urls=[]
user_id = sp.current_user()["id"]
for song in song_names_list:
    result = sp.search(q=f"track:{song},year:{year}",type="track")
    try:
        uri=result["tracks"]["items"][0]["uri"]
        spotify_urls.append(uri)
    except IndexError:
        print(IndexError)
playlist = sp.user_playlist_create(user=user_id,name=f"{date} Billboard Hot 100",public=False)
sp.playlist_add_items(playlist_id=playlist["id"],items=spotify_urls)
print(spotify_urls)

