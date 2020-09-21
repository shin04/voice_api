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
```

response
```
{
    "db": 0, # 音量
    "db_max": 0, # 最大音量
    "f0": [], # 基本周波数（高さ）
    "speaking_rate": [], # 発話速度
    "message": "success",
    "success": true
}
```
