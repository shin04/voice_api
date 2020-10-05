import unittest
import sys
import io
import os
sys.path.append(os.path.abspath(".."))

import app  # noqa


class TestStatusCode(unittest.TestCase):
    def setUp(self):
        print('Start Test About Response Body')
        app.app.config['TESTING'] = True
        app.app.config.from_json('config/app_config.json')
        self.client = app.app.test_client()

    def tearDown(self):
        print('End Test')

    def test_hello(self):
        print('[GET] /hello')
        res = self.client.get('/')
        json_data = res.get_json()
        message = json_data['message']
        self.assertEqual(message, 'hello world')

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
        json_data = res.get_json()

        nums = []
        nums.append(len(json_data['amplitude']))
        nums.append(len(json_data['pitch']))
        nums.append(len(json_data['speaking_rate']))
        nums.append(len(json_data['speaking_time']))

        self.assertEqual(nums, [1, 1, 1, 1])

        # message = json_data['error']['message']
        # self.assertEqual(message, 'parameter [file] is not found')


if __name__ == '__main__':
    unittest.main()
