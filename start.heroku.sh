# For setting credentials in heroku
echo Setting...
mkdir credentials
touch credentials/voice-recognition.json
echo ${GOOGLE_APPLICATION_CREDENTIALS} > credentials/voice-recognition.json
python app.py
