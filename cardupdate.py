from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from youtube_search import YoutubeSearch

PLAYLISTS = [
    [
        "eng",
        "https://open.spotify.com/playlist/7rE1ztUke1WZP2dAGh0Fex?si=6a5acdec3b5245ce",
        "PLtD4KkuvbBvCuvhdoTimMzpTQVJxVIhpB",
    ],
      [
        "Chill soft EDM",
        "https://open.spotify.com/playlist/4018yqdYFAGJq2tn0bYFCu?si=efaa1ad5a4b14cfe",
        "PLtD4KkuvbBvCUt9TtaKMd5P0-X7gcMxgl",
    ],
]
client_credentials_manager = SpotifyClientCredentials(
    client_id="4c2d042400724ba9a95fd33593beaa97",
    client_secret="fe85c1684601493e9b6294285a62d08d",
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


CONTAINER = []
for playlist in PLAYLISTS:
    Name, Link, playlistid = playlist
    playlistcard = []
    count = 0
    PlaylistLink = "http://www.youtube.com/watch_videos?video_ids="
    for i in sp.playlist_tracks(Link)["items"]:
        if count == 50:
            break
        try:
            song = i["track"]["name"] + i["track"]["artists"][0]["name"]
            songdic = (YoutubeSearch(song, max_results=1).to_dict())[0]
            playlistcard.append(
                [
                    songdic["thumbnails"][0],
                    songdic["title"],
                    songdic["channel"],
                    songdic["id"],
                ]
            )
            PlaylistLink += songdic["id"] + ","
        except:
            continue
        count += 1

    from urllib.request import urlopen

    req = urlopen(PlaylistLink)
    PlaylistLink = req.geturl()
    print(PlaylistLink)
    PlaylistId = PlaylistLink[PlaylistLink.find("list") + 5 :]

    CONTAINER.append([Name, playlistcard, playlistid])

import json

json.dump(CONTAINER, open("card.json", "w"), indent=6)
