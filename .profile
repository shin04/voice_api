# For setting credentials in heroku
mkdir ./credentials
touch ./credentials/voice-recognition.json
echo ${GOOGLE_APPLICATION_CREDENTIALS} > ./credentials/voice-recognition.json
pwd