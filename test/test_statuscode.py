import unittest
import sys
import os
sys.path.append(os.path.abspath(".."))

import app  # noqa


class TestStatusCode(unittest.TestCase):
    def setUp(self):
        print('Start Test About Status Code')
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()

    def tearDown(self):
        print('End Test')

    def test_hello(self):
        print('[GET] /')
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

    def test_analyze(self):
        print('[POST] /analyze')
        res = self.client.post('/analyze', json={
            'people_num': 2
        })
        self.assertEqual(res.status_code, 400)


if __name__ == '__main__':
    unittest.main()
