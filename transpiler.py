from spotipy import Spotify
import random

class Transpiler:
    def __init__(self, spotify: Spotify) -> None: #{{{1
   
        #read in songs that we can add to playlist
        with open('tracks.txt') as f: #{{{2
            self.songs = []
            for line in f:
                self.songs.append(line.strip().split(','))
        #2}}}
    
        self.sp = spotify
    #1}}}

    #get a random song of a particular genre.
    def get_random_song(self, genre: str) -> str: #{{{1
        #choose a random song of the given genre from the available choices.
        song = random.choice(list(filter(lambda x: x[0] == genre, self.songs)))
        return song
    #1}}}

    #convert brainfuck char to spotify song data.
    def bf_to_spotify(self, char: str) -> str | None: #{{{1
        song = None
        #translate to slang song if there is a match.
        match char: #{{{2
            case '>':
                song = self.get_random_song('chillhop')
            case '<':
                song = self.get_random_song('study beats')
            case '+':
                song = self.get_random_song('lo-fi jazzhop')
            case '-':
                song = self.get_random_song('lo-fi beats')
            case '.':
                song = self.get_random_song('focus beats')
            case ',':
                song = self.get_random_song('hamburg hip hop')
            case '[':
                song = self.get_random_song('jazz boom bap')
            case ']':
                song = self.get_random_song('greek downtempo')
        #2}}}
        return song

    #1}}}

    #go through brainfuck program and convert to slang.
    def transpile(self, playlist: str, bf) -> None: #{{{1
        for line in bf:
            for char in line:
                #convert bf char to slang instruction, if song has a valid conversion.
                song = self.bf_to_spotify(char)
                if song:
                    self.sp.playlist_add_items(playlist,[song[2]])
        #1}}}

#if being run directly, use command line arguments.
if __name__ == '__main__': #{{{1
    from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth
    import sys
    import json

    #log into spotify.
    with open('.creds/creds.json') as credfile:
        creds = json.load(credfile)
        sp = Spotify(auth_manager=SpotifyOAuth(client_id=creds['CLIENT_ID'], client_secret=creds['CLIENT_SECRET'], scope='playlist-modify-public',redirect_uri='http://127.0.0.1:9000'))

    #read brainfuck program into a list.
    with open(sys.argv[1]) as f:
        bf = [line.strip() for line in f.readlines()]
    
    #transpile brainfuck to slang.
    playlist = sys.argv[2]
    tpiler = Transpiler(sp)
    tpiler.transpile(playlist, bf)
#1}}}
