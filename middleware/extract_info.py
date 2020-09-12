import pyworld as pw
from pydub import AudioSegment
from pydub.silence import split_on_silence
import numpy as np

import os

def main(filename, cfg):
    print('analyze')

    file_path = cfg['FILE_PATH'] + '/' + filename

    res = {
        'db': [],
        'db_max': [],
        'f0': [],
        # 'sp': [],
        # 'ap': []
    }

    if not os.path.exists(file_path):
        return res

    sound = AudioSegment.from_file(file_path, 'mp3')

    fs = sound.frame_rate
    data = np.array(sound.get_array_of_samples()).astype(np.float)

    db = sound.rms # デシベル
    db_max = sound.max
    _f0, _time = pw.dio(data, fs)    # 基本周波数の抽出
    f0 = pw.stonemask(data, _f0, _time, fs)  # 基本周波数の修正
    # sp = pw.cheaptrick(data, f0, _time, fs)  # スペクトル包絡の抽出
    # ap = pw.d4c(data, f0, _time, fs)  # 非周期性指標の抽出

    res['db'] = db
    res['db_max'] = db_max
    res['f0'] = f0.tolist()
    # res['sp'] = sp.tolist()
    # res['ap'] = ap.tolist()

    os.remove(file_path)

    return res

if __name__ == "__main__":
    pass