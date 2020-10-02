# Set Up

## 1.

Add to credential json file to credentials folder

## 2.

Environment construction and server startup

### use docker

```
$ docker build -t voice_api .

$ docker run -it --name voice_api -p 5000:5000 voice_api /bin/bash
```

### dont use docker

```
$ brew install ffmpeg # macos
$ sudo apt-get install ffmpeg # ubuntu

$ python -m venv [env name]
$ source [env name]/bin/activate
$ pip install -r requirement.txt

$ sh start.sh
```

# Usage

## localhost:5000/analyze

params

```
files: mp3 file
person_num: number of speakers
```

response

```
{
    "amplitude": [
        {
            "1"(speaker_tag): [
                    [amplitude list (float)],
                    ...
                ]
        },
        ...
    ],
    "pitch": [
        {
            "1"(speaker_tag): [
                    [amplitude list (float)],
                    ...
                ]
        },
        ...
    ]
    "speaking_rate": [
        {"1"(speaker_tag): speaking_rate(float)},
        ...
    ],
    speaking_time: [
        {speaker_tag: [[0,1],[3,5],,,[start_time, stop_time]]},
        ...
    ]
}
```
