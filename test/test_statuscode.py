import unittest
import sys
import io
import os
sys.path.append(os.path.abspath(".."))

import app  # noqa


class TestStatusCode(unittest.TestCase):
    def setUp(self):
        print('Start Test About Status Code')
        app.app.config['TESTING'] = True
        app.app.config.from_json('config/app_config.json')
        self.client = app.app.test_client()

    def tearDown(self):
        print('End Test')

    def test_hello(self):
        print('[GET] /')
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

    def test_analyze(self):
        print('[POST] /analyze')
        file_name = './sample_voices/sample1.mp3'
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
        voice_file = (io.BytesIO(content), 'test.mp3')
        res = self.client.post('/analyze', data={
            'files': voice_file,
            'people_num': 1
        })
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
