import os
import lyricsgenius
import random
"""
Állítsd be a "GENIUS_TOKEN" környezeti változót! URL: https://genius.com/api-clients
"""
GENIUS = lyricsgenius.Genius(os.getenv('GENIUS_TOKEN'), verbose=False)


def get_album_id():  # getting the album id
    artist = GENIUS.search_artist(input('Kedvenc előadód: '), max_songs=0)
    albums = GENIUS.artist_albums(artist_id=artist.to_dict()['id'])
    print('\nAlbumok:')
    for album in albums['albums']:
        print(album['name'])
    album_name = input('\nVálassz: ').lower()
    for album in albums['albums']:
        if album_name == album['name'].lower():
            return album['id']


def get_song_and_lyrics(album_id):  # getting the title and lyrics
    songs = GENIUS.album_tracks(album_id=album_id)
    song = random.choice(songs['tracks'])
    song_id = song['song']['id']
    song_name = song['song']['title']
    raw_lyrics = GENIUS.lyrics(song_id=song_id)
    return song_name, raw_lyrics


def clean_lyrics(raw_lyrics):  # cleans the lyrics from useless things
    lyrics = raw_lyrics.split('\n')
    for index in range(len(lyrics[0])):
        if lyrics[0][index:index + 6] == 'Lyrics':
            lyrics[0] = lyrics[0][index + 6:]
            break
    for index in range(len(lyrics)):
        for index2 in range(len(lyrics[index])):
            if lyrics[index][index2:index2 + 19] == 'You might also like':
                lyrics[index] = lyrics[index][:index2] + lyrics[index][index2 + 19:]
                break
    for index in range(len(lyrics[-1])):
        if lyrics[-1][index:index + 5] == 'Embed':
            index2 = index
            while True:
                index2 -= 1
                if not lyrics[-1][index2].isnumeric():
                    lyrics[-1] = lyrics[-1][:index2 + 1]
                    break
            break
    return '\n'.join(lyrics)


def game(title, lyrics):  # running the actual game
    print('\n\nZeneszöveg:\n' + lyrics)
    while True:
        guess = input('\nTippelj: ').lower()
        if guess == title.lower():
            print('Eltaláltad. Gratula!')
            break
        elif guess == 'szabad a gazda':
            print('Béna vagy, itt a megfejtés: ' + title)
            break
        else:
            print('Nem jó!')


def main():
    print('Ez a program bekéri a kedvenc előadódat, majd egy választott albumának egyik számát kell kitalálni a '
          'zene szövegének felhasználásával.\nHa fel akarod adni, akkor csak írd be hogy "szabad a gazda".')
    song = get_song_and_lyrics(get_album_id())
    game(song[0], clean_lyrics(song[1]))


main()
