from spotipy import Spotify

#grammer:
#genre = "chillhop" -> move data pointer to right
#"study beats" -> move data pointer to left
#"lo-fi jazzhop" -> Increment data at pointer.
#"lo-fi beats" -> Decrement data at  pointer.
#"focus beats" -> Output byte at data pointer.
#"hamburg hip hop" -> Get one byte of input and store at current data cell. Input should be ASCII encoded.
#"jazz boom bap" -> If current cell is zero, jump to command after "lo-fi jazzhop".
#"greek downtempo" -> If current cell is nonzero, jump to command after "jazz boom bap".

class Interpreter:
    def __init__(self, sp: Spotify) -> None: #{{{1
        self.data = bytearray(1000)
        self.inst_ptr = 0
        self.data_ptr = 0
        self.inst = []
        self.source = 0
        self.nest = []
    #1}}}

    #Return a tuple with data we care about.
    def lex(self, data: dict) -> tuple: #{{{1

        #Get the song name.
        name = data['name']

        #Get the genre of the artist.
        artist_uri = data['artists'][0]['uri']
        artist = sp.artist(artist_uri)
        try:
            genre = artist['genres'][0]
        except IndexError:
            #Maybe change this to a custom error??
            raise RuntimeError(f"\x1b[1;31mLEXING ERROR: artist '{artist['name']}' has no genre.\x1b[0m")

        return (genre, name)
    #1}}}

    def parse(self, source: str) -> None: #{{{1
        self.source = source
        tracks = sp.playlist_tracks(source)
        offset = 0
        while offset <= tracks['total']:
            for track in tracks['items']:
                self.inst.append(self.lex(track['track']))
            offset += 100
            tracks = sp.playlist_tracks(source,offset=offset) 
    #1}}}

    def interp(self, command: tuple) -> None: #{{{1
        match command[0]:
            case 'chillhop':
                self.data_ptr += 1
            case 'study beats':
                self.data_ptr -= 1
            case 'lo-fi jazzhop':
                self.data[self.data_ptr] += 1
            case 'lo-fi beats':
                self.data[self.data_ptr] -= 1
            case 'focus beats':
                print(chr(self.data[self.data_ptr]), end='')
            case 'hamburg hip hop':
                self.data[self.data_ptr] = ord(input()[0])
            case 'jazz boom bap':
                if self.data[self.data_ptr] == 0:
                    while True:
                        self.inst_ptr += 1
                        if self.inst[self.inst_ptr][0] == 'jazz boom bap':
                            self.nest.append(True)
                        if self.inst[self.inst_ptr][0] == 'greek downtempo':
                            if len(self.nest) == 0:
                                break
                            else:
                                self.nest.pop()

            case 'greek downtempo':
                if self.data[self.data_ptr] != 0:
                    while True:
                        self.inst_ptr -= 1
                        if self.inst[self.inst_ptr][0] == 'greek downtempo':
                            self.nest.append(True)
                        if self.inst[self.inst_ptr][0] == 'jazz boom bap':
                            if len(self.nest) == 0:
                                break
                            else:
                                self.nest.pop()

    #1}}}

    def run(self) -> None: #{{{1
        while self.inst_ptr < len(self.inst):
            self.interp(self.inst[self.inst_ptr])
            self.inst_ptr += 1

    #1}}}

if __name__ == '__main__': #{{{1
    import sys
    import json
    from spotipy.oauth2 import SpotifyClientCredentials


    with open('.creds/creds.json') as credfile:
        creds = json.load(credfile)
        auth = SpotifyClientCredentials(client_id=creds['CLIENT_ID'], client_secret=creds['CLIENT_SECRET'])
        sp = Spotify(client_credentials_manager=auth)
        interp = Interpreter(sp)
        interp.parse(sys.argv[1])
        #print(interp.inst)
        interp.run()
#1}}}

