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
        self.client = app.app.test_client()

    def tearDown(self):
        print('End Test')

    def test_hello(self):
        res = self.client.get('/')
        json_data = res.get_json()
        message = json_data['message']
        self.assertEqual(message, 'hello world')

    def test_analyze(self):
        print('[POST] /analyze')
        voice_file = (io.BytesIO(b'this is test mp3'), 'test.mp3')
        res = self.client.post('/analyze', data={
            'people_num': 2
        })
        json_data = res.get_json()
        print(json_data)
        message = json_data['error']['message']
        self.assertEqual(message, 'parameter [file] is not found')


if __name__ == '__main__':
    unittest.main()
