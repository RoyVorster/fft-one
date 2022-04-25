import os.path
import youtube_dl

from scipy.io import wavfile

EXT = 'wav'
FNAME = 'data/%(id)s.%(ext)s'

OPTS = {
    'format': 'bestaudio/best',
    'outtmpl': FNAME,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': EXT,
    }],
}

def get_f_name(vid):
    return FNAME % {'id': vid, 'ext': EXT}

def download_data(vid):
    with youtube_dl.YoutubeDL(OPTS) as ydl:
        data = ydl.extract_info(f'https://www.youtube.com/watch?v={vid}', download=True)
        print(data)

def load_data(vids):
    data = {}
    for vid in vids:
        f_name = get_f_name(vid)
        if not os.path.exists(f_name):
            download_data(vid)
    
        # And get data directly from .wav
        _, data = wavfile.read(f_name)
        data[vid] = data

    return data

if __name__ == '__main__':
    vids = ['ugJ-rYS-9JU']
    load_data(vids)

