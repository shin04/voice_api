import pyworld as pw
from pydub import AudioSegment
from pydub.silence import split_on_silence
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from mutagen.mp3 import MP3
import numpy as np

import os
import io
import re


def get_googleapi_res(file_path):
    audio = MP3(file_path)
    speaking_time = audio.info.length

    client = speech_v1p1beta1.SpeechClient()

    language_code = "ja-JP"
    sample_rate_hertz = 44100
    encoding = enums.RecognitionConfig.AudioEncoding.MP3
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
        "enable_speaker_diarization": True,
        "diarization_speaker_count": 2
    }

    with io.open(file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}
    response = client.recognize(config, audio)

    return response, speaking_time


def separate_people(response):
    result = response.results[-1]
    words_info = result.alternatives[0].words

    people_infos = []
    for _ in range(2):
        person_infos = []
        people_infos.append(person_infos)
    for word_info in words_info:
        m = re.search(r'(.*)\|.*$', word_info.word)
        word = m.group(1)
        speaker_tag = int(word_info.speaker_tag)
        start_time = float(word_info.start_time.seconds) + \
            float(word_info.start_time.nanos)/(10**9)
        stop_time = float(word_info.end_time.seconds) + \
            float(word_info.end_time.nanos)/(10**9)

        if len(people_infos[speaker_tag-1]) != 0 and people_infos[speaker_tag-1][-1]["stop_time"] == start_time:
            people_infos[speaker_tag-1][-1]["word"] += word
            people_infos[speaker_tag-1][-1]["stop_time"] = stop_time
        else:
            person_info = {
                "word": word,
                "speaker_tag": speaker_tag,
                "start_time": start_time,
                "stop_time": stop_time
            }
            people_infos[speaker_tag-1].append(person_info)

    return people_infos


def extract_speed(response, speaking_time):
    transcripts = []
    for result in response.results:
        alternative = result.alternatives[0]
        transcripts.append(alternative.transcript)

    word_counts = [0] * len(transcripts)
    for i, sentence in enumerate(transcripts):
        word_counts[i] = len(sentence)

    speaking_rate = []
    for i in range(len(transcripts)):
        speaking_rate.append(word_counts[i]/speaking_time)

    res = {}
    res['speaking_rate'] = speaking_rate

    return res


# def to_db(x, N):
#     pad = np.zeros(N//2)
#     pad_data = np.concatenate([pad, x, pad])
#     rms = np.array([np.sqrt((1/N) * (np.sum(pad_data[i:i+N]))**2)
#                     for i in range(len(x))])
#     return 20 * np.log10(rms)


def extract_pitch_and_db(sound):
    fs = sound.frame_rate
    data = np.array(sound.get_array_of_samples()).astype(np.float)
    # data = data / 32768.0

    amplitude = data  # 振幅
    # N = 1024  # デシベル変換時のサンプリング数
    # db = to_db(amplitude, N)  # デシベルに変換
    # db = sound.rms  # デシベル（平均）
    # db_max = sound.max  # デシベル（最大）
    _f0, _time = pw.dio(data, fs)    # 基本周波数の抽出
    f0 = pw.stonemask(data, _f0, _time, fs)  # 基本周波数の修正
    # sp = pw.cheaptrick(data, f0, _time, fs)  # スペクトル包絡の抽出
    # ap = pw.d4c(data, f0, _time, fs)  # 非周期性指標の抽出

    res = {}
    res['amplitude'] = amplitude.tolist()
    # res['db'] = db
    # res['db_max'] = db_max
    res['f0'] = f0.tolist()
    # res['sp'] = sp.tolist()
    # res['ap'] = ap.tolist()

    return res


def main(filename, cfg):
    file_path = cfg['FILE_PATH'] + '/' + filename
    response, speaking_time = get_googleapi_res(file_path)
    people_info = separate_people(response)
    print(people_info)

    res = {}

    if not os.path.exists(file_path):
        return res

    sound = AudioSegment.from_file(file_path, 'mp3')
    res_1 = extract_pitch_and_db(sound)
    res.update(res_1)

    res_2 = extract_speed(response, speaking_time)
    res.update(res_2)

    os.remove(file_path)

    return res


if __name__ == "__main__":
    pass
