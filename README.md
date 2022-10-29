# *slang*: the Spotify programming language.
slang is a programming language where valid code is input through a Spotify playlist.

**ATTN: IT LOOKS LIKE SOME OF THE ARTISTS IN `tracks.txt` HAVE CHANGED THIER GENRE. THEREFORE, SOME SLANG PROGRAMS THAT ONCE WORKED MAY NOT WORK ANYMORE.**

slang is a Turing Tarpit language, where different instructions are encoded by the genre of the first artist of a song.
The only internal data structure is an array of binary data, which is interacted with using eight instructions.
The instructions are encoded using subgenres of lo-fi.

|genre|action|
|-----|------|
|chillhop|move data pointer to right.|
|study beats|move data pointer to left.|
|lo-fi jazzhop|increment data at pointer.|
|lo-fi beats|decrement data at  pointer.|
|focus beats|output byte at data pointer.|
|hamburg hip hop|get one byte of input and store at current data cell. Input should be ASCII encoded.|
|jazz boom bap|if current cell is zero, jump to command after "lo-fi jazzhop".|
|greek downtempo|if current cell is nonzero, jump to command after "jazz boom bap".|

You may notice these instructions are similar to [brainfuck](https://en.wikipedia.org/wiki/Brainfuck). This would be correct!
slang is actually bijective to brainfuck. Because of this, I also wrote a transpiler from brainfuck to slang,`transpiler.py`.

# Setup
Setup is pretty easy. First, install the modules in `requirements.txt`. Second, generate keys in the [Spotify developer dashboard](https://developer.spotify.com/dashboard). Here, you will need to generate a `Client ID` and `Client Secret`. You will also need to set a `redirect uri` of your app to `http://127.0.0.1:9000`. After this, create a `.creds` folder in the same directory as the interpreter/transpiler. In this folder, create a `creds.json` with the following content.

```json
{
"CLIENT_ID":"client_id_here"
"CLIENT_SECRET":"client_secret_here"
}
```

After this, you are good to go!

# Running
To run the interpreter, simply do
```
python3 interperter.py source_code_playlist_url
```

To transpile from brainfuck to slang, run
```
python3 transpiler.py /path/to/bf/code destination_code_playlist_url
```

Enjoy!
