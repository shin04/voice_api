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


def get_googleapi_res(voice_byte, people_num):
    client = speech_v1p1beta1.SpeechClient()

    language_code = "ja-JP"
    sample_rate_hertz = 44100
    encoding = enums.RecognitionConfig.AudioEncoding.MP3
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
        "enable_speaker_diarization": True,
        "diarization_speaker_count": people_num
    }

    content = voice_byte
    audio = {"content": content}
    response = client.recognize(config, audio)

    return response


def separate_people(response, people_num):
    result = response.results[-1]
    words_info = result.alternatives[0].words

    people_infos = []
    for _ in range(people_num):
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


def get_speaking_time(people_infos):
    speaking_times = []
    for person_infos in people_infos:
        speaking_times_dict = {}
        speaking_times_dict[person_infos[0]['speaker_tag']] = []
        for person_info in person_infos:
            person_speaking_times = [
                person_info["start_time"],
                person_info["stop_time"]
            ]
            speaking_times_dict[person_info["speaker_tag"]].append(
                person_speaking_times)
        speaking_times.append(speaking_times_dict)

    return speaking_times


def calc_speed(people_infos):
    res = []
    for i, person_infos in enumerate(people_infos):
        time = 0.
        words = ""
        for person_info in person_infos:
            time += person_info['stop_time'] - person_info['start_time']
            words += person_info['word']
        speaking_rate = 0.
        if time != 0.:
            speaking_rate = len(words) / time
        res.append({str(i+1): speaking_rate})

    return res


def sound_to_numpy(sound):
    fs = sound.frame_rate
    # data = np.array(sound.get_array_of_samples()).astype(np.float)
    data = np.array(sound.get_array_of_samples())
    # data = data / 32768.0
    return data, fs


def extract_pitch(data, fs):
    _f0, _time = pw.dio(data.astype(np.float), fs)    # 基本周波数の抽出
    f0 = pw.stonemask(data.astype(np.float), _f0, _time, fs)  # 基本周波数の修正
    # sp = pw.cheaptrick(data, f0, _time, fs)  # スペクトル包絡の抽出
    # ap = pw.d4c(data, f0, _time, fs)  # 非周期性指標の抽出

    return f0.tolist()


def extract_sound_by_person(people_infos, sound):
    sounds = {}
    for i, person_infos in enumerate(people_infos):
        person_sounds = []
        for person_info in person_infos:
            start_time = person_info['start_time']  # s
            stop_time = person_info['stop_time']    # s

            sec_sound = sound[start_time*1000:stop_time*1000]
            # sec_sound.export("sound_1.mp3", format="mp3")
            person_sounds.append(sec_sound)
        # sounds.append({str(i+1): person_sounds})
        sounds[str(i+1)] = person_sounds

    return sounds


def extract_info(voice_file, filename, cfg, people_num):
    voice_byte = voice_file.read()
    response = get_googleapi_res(voice_byte, people_num)
    people_infos = separate_people(response, people_num)

    sound = AudioSegment.from_mp3(io.BytesIO(voice_byte))
    # data, fs = sound_to_numpy(sound)

    speaking_rates = calc_speed(people_infos)
    sounds_by_person = extract_sound_by_person(people_infos, sound)

    speaking_times = get_speaking_time(people_infos)

    pitches = []
    amplitudes = []
    for speaker_tag, person_sounds in sounds_by_person.items():
        person_pitches = []
        person_amplitudes = []
        for sound in person_sounds:
            data, fs = sound_to_numpy(sound)
            pitch = extract_pitch(data, fs)
            person_pitches.append(pitch)
            person_amplitudes.append(data.tolist())
        pitches.append({speaker_tag: person_pitches})
        amplitudes.append({speaker_tag: person_amplitudes})

    res = {}

    res['speaking_time'] = speaking_times
    res['amplitude'] = amplitudes
    res['pitch'] = pitches
    res['speaking_rate'] = speaking_rates

    return res


if __name__ == "__main__":
    pass
