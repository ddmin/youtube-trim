#!/usr/bin/python

# yt-trim: download and label mp3 files
# Dependencies: ffmpeg, yt-dlp

from os.path import exists
import subprocess

SONG_FILE = 'songs.trim'

with open(SONG_FILE, 'r') as f:
    songs = f.read().split('\n')[:-1]

songs = list(filter(lambda x: x, songs))
songs = list(filter(lambda x: x[0] != '#', songs))

# check file syntax
print(f"Checking {SONG_FILE}...\n")
for song in songs:
    vals = song.split(';')
    try:
        assert(vals[0])
        assert(vals[1])
        assert(vals[2])
        assert(vals[3])
        assert(vals[4])
    except:
        print(f'Error in line: `{song}`')
        exit()

for song in songs:
    vals = song.split(';')
    print(f'Link: {vals[0]}')
    print(f'Name: {vals[1]}')
    print(f'Artist: {vals[2]}')
    print(f'Album: {vals[3]}')
    print(f'Time: {vals[4]}')
    print('='*60)

    to_trim = False

    try:
        times = vals[4].split('-')
        start_time = times[0]
        end_time = times[1]
        to_trim = True
    except:
        pass

    subprocess.run(
        [
            'yt-dlp',
            '-x',
            '--audio-format', 'mp3',
            '-o', 'song.mp3',
            vals[0],
        ]
    )

    print('='*60)

    filename = f'[{vals[3]}] {vals[1]}'

    if to_trim:
        subprocess.run(
            [
                'ffmpeg',
                '-i', 'song.mp3',
                '-ss', f'{start_time}', '-to', f'{end_time}',
                'song2.mp3',
            ]
        )

        subprocess.run(['rm', 'song.mp3'])

        subprocess.run(['mv', 'song2.mp3', filename+'_pre.mp3'])

    else:

        subprocess.run(['mv', 'song.mp3', filename+'_pre.mp3'])

    if exists(f'./Art/{vals[3]}.jpg'):
        art = f'./Art/{vals[3]}.jpg'
    elif exists(f'./Art/{vals[3]}.png'):
        art = f'./Art/{vals[3]}.png'
    else:
        art = 'Art/default.jpg'

    subprocess.run(
        [
            'ffmpeg',
            '-y',
            '-i', f'{filename}_pre.mp3',
            '-c', 'copy',
            '-metadata', f'album={vals[3]}',
            '-metadata', f'artist={vals[2]}',
            '-metadata', f'title={vals[1]}',
            f'{filename}_pre_pre.mp3',
        ]
    )

    subprocess.run(
        [
            'ffmpeg',
            '-i', filename+'_pre_pre.mp3',
            '-i', art,
            '-map_metadata', '0',
            '-map', '0',
            '-map', '1',
            '-acodec', 'copy',
            filename+'.mp3',
        ]
    )

    subprocess.run(['rm', filename+'_pre.mp3'])
    subprocess.run(['rm', filename+'_pre_pre.mp3'])

    print('='*60)

print(f"Total: {len(songs)}")
