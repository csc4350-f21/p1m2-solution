import flask
import requests
import json
import sys
import os
sys.path.append(os.path.abspath("."))
import random
import base64
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = flask.Flask(__name__)


MARKET = "US"

def get_access_token():
	auth = base64.standard_b64encode(bytes(f"{os.getenv('SPOTIFY_CLIENT_ID')}:{os.getenv('SPOTIFY_CLIENT_SECRET')}", "utf-8")).decode("utf-8")
	response = requests.post(
		"https://accounts.spotify.com/api/token",
		headers={"Authorization": f"Basic {auth}"},
		data={"grant_type": "client_credentials"}
	)
	json_response = response.json()
	return json_response["access_token"]

@app.route('/')
def index():
	access_token = get_access_token()

	artist_ids = [
		"4UXqAaa6dQYAk18Lv7PEgX",  # FOB
		"3jOstUTkEu2JkjvRdBA5Gu",  # Weezer
		"7oPftvlwr6VrsViSDV7fJY",  # Green Day
	]
	artist_id = random.choice(artist_ids)

	response = requests.get(
		f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
		headers={"Authorization": f"Bearer {access_token}"},
		params={"market": MARKET}
	)
	json_response = response.json()
	track_json = random.choice(json_response["tracks"])
	song_name = track_json["name"]
	song_artist = ", ".join([artist["name"] for artist in track_json["artists"]])
	song_image_url = track_json["album"]["images"][0]["url"]
	preview_url = track_json["preview_url"]

	genius_response = requests.get(
		"https://api.genius.com/search",
		headers={"Authorization": f"Bearer {os.getenv('GENIUS_AUTH_TOKEN')}"},
		params={"q": song_name}
	)
	genius_response_json = genius_response.json()
	genius_url = genius_response_json["response"]["hits"][0]["result"]["url"]

	return flask.render_template(
    	"index.html",
    	song_name=song_name,
    	song_artist=song_artist,
    	song_image_url=song_image_url,
    	preview_url=preview_url,
    	genius_url=genius_url
    )

app.run(
	host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)