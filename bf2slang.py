from spotipy import Spotify
import sys
import json
import random
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth

#auth {{{1
with open('.creds/creds.json') as credfile:
    creds = json.load(credfile)
    sp = Spotify(auth_manager=SpotifyOAuth(client_id=creds['CLIENT_ID'], client_secret=creds['CLIENT_SECRET'], scope='playlist-modify-public',redirect_uri='http://127.0.0.1:9000'))
#1}}}

#read in songs that we can add to playlist {{{1
with open('tracks.txt') as f:
    genres = []
    for line in f:
        genres.append(line.strip().split(','))
#1}}}

def get_random_song(genre: str) -> str: #{{{1
    song = random.choice(list(filter(lambda x: x[0] == genre, genres)))
    return song
#1}}}

def bf_to_spotify(char: str) -> str | None: #{{{1
    song = None
    match char: #{{{2
        case '>':
            song = get_random_song('chillhop')
        case '<':
            song = get_random_song('study beats')
        case '+':
            song = get_random_song('lo-fi jazzhop')
        case '-':
            song = get_random_song('lo-fi beats')
        case '.':
            song = get_random_song('focus beats')
        case ',':
            song = get_random_song('hamburg hip hop')
        case '[':
            song = get_random_song('jazz boom bap')
        case ']':
            song = get_random_song('greek downtempo')

    if song:
        return song
    return None
    #2}}}

#1}}}

#go through brainfuck program and convert to slang. {{{1
bf = sys.argv[1]
playlist = sys.argv[2]

with open(bf) as f:
    for line in f:
        for char in line:
           song = bf_to_spotify(char) 
           if song:
               sp.playlist_add_items(playlist,[song[2]])
               print(f'bfchar = {char} --> added {song[0]} {song[1]}')
#1}}}
