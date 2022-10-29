from spotipy import Spotify

#grammer:
#genre -> action
#"chillhop" -> move data pointer to right
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
        #instruction pointer (index we are focused on in instruction list).
        self.inst_ptr = 0
        #data pointer (index we are focused on in data array).
        self.data_ptr = 0
        self.inst = []
        #url of source code playlist.
        self.source = ''
        #the list is used as a "stack" which we use to match each "jazz boom bap" to "greek downtempo" for while loops.
        self.nest = []
    #1}}}

    #take in a dictionary of song data from spotipy and return a tuple with data we care about.
    def lex(self, data: dict) -> tuple: #{{{1

        #get the song name.
        name = data['name']

        #get the first artist.
        artist_uri = data['artists'][0]['uri']
        artist = sp.artist(artist_uri)
        try:
            #get the first genre.
            genre = artist['genres'][0]
        except IndexError:
            raise RuntimeError(f"\x1b[1;31mLEXING ERROR: artist '{artist['name']}' has no genre.\x1b[0m")

        return (genre, name)
    #1}}}

    #take in a soure playlist uri, and fill the instruction stack.
    def parse(self, source: str) -> None: #{{{1
        #save source uri.
        self.source = source

        #grab tracks from playlist.
        tracks = sp.playlist_tracks(source)

        #the "offset" is needed here as spotipy will return you tracks in batches of 100.
        #by default, it starts at zero.
        #we do this until we run out.
        offset = 0
        while offset <= tracks['total']:
            #for each track returned "lex" it, and add to instructions.
            for track in tracks['items']:
                self.inst.append(self.lex(track['track']))

            #get next batch of tracks.
            offset += 100
            tracks = sp.playlist_tracks(source,offset=offset) 
    #1}}}

    #execute an instruction.
    def interp(self, command: tuple) -> None: #{{{1
        print(command[0], command[1]) 
        #take the corresponding action based on the genre.
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
                #chr() turns a byte into its corresponding ascii char.
                print(chr(self.data[self.data_ptr]), end='')
            case 'hamburg hip hop':
                #ord() takes a ascii char and returns its code.
                self.data[self.data_ptr] = ord(input()[0])
            case 'jazz boom bap':
                if self.data[self.data_ptr] == 0:
                    #look for the matching "greek downtempo".
                    while True:
                        self.inst_ptr += 1
                        breakpoint()
                        #push to the stack if we see the beginning of another loop.
                        if self.inst[self.inst_ptr][0] == 'jazz boom bap':
                            self.nest.append(True)
                        if self.inst[self.inst_ptr][0] == 'greek downtempo':
                            #if the stack is empty, then we are at the downtempo which matches this boom bap!
                            if len(self.nest) == 0:
                                break
                            #otherwise, pop from the stack when we see the end of a loop.
                            else:
                                self.nest.pop()
            
            #very similar to the "jazz boom bap" case, except moves backwards towards a "jazz boom bap".
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

    #run the interpreter.
    def run(self) -> None: #{{{1
        #execute each instruction in the list.
        while self.inst_ptr < len(self.inst):
            self.interp(self.inst[self.inst_ptr])
            self.inst_ptr += 1

    #1}}}

#when run standalone, this script will take a source code link and run it.
if __name__ == '__main__': #{{{1
    import sys
    import json
    from spotipy.oauth2 import SpotifyClientCredentials

    #load credentials from external file.
    with open('.creds/creds.json') as credfile:
        creds = json.load(credfile)

        #log into spotify.
        auth = SpotifyClientCredentials(client_id=creds['CLIENT_ID'], client_secret=creds['CLIENT_SECRET'])

        #create a spotipy object to interact with spotify.
        sp = Spotify(client_credentials_manager=auth)

        #create an interpreater as pass stdin.
        interp = Interpreter(sp)
        interp.parse(sys.argv[1])
        interp.run()
#1}}}
