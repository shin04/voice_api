# For setting credentials in heroku
echo Setting...
mkdir credentials
touch credentials/voice-recognition.json
echo ${GOOGLE_APPLICATION_CREDENTIALS} > credentials/voice-recognition.json
test=`ls -la`
echo $test
python app.py