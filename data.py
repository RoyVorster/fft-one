import os.path
import youtube_dl

from scipy.io import wavfile
import numpy as np

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

# Quick wrapper
class AudioData:
    def __init__(self, vid):
        self.vid, self.f_name = vid, get_f_name(vid)

        # Download if not exists
        if not os.path.exists(self.f_name):
            download_data(self.vid)

        # And get .wav file
        self.reload()

    def reload(self):
        self.fs, self.data = wavfile.read(self.f_name)
        self.dt = 1/self.fs

        self.n = self.data.shape[0]
        self.time = np.arange(0, self.n/self.fs, self.dt)

def load_data(vids):
    return [AudioData(vid) for vid in vids]

