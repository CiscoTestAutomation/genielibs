#!/usr/bin/env python
import os
import binascii
import tempfile
import unittest
import requests

from genie.libs.filetransferutils import FileServer
from pyats.datastructures import AttrDict
from pyats.utils.secret_strings import SecretString, to_plaintext


def encode_multipart_formdata(data):
    boundary = '-' * 25 + binascii.hexlify(os.urandom(16)).decode('ascii')

    body = ''
    if not isinstance(data, list):
        data = [data]
    for content in data:
        body += '--{boundary}\r\n'\
            'Content-Disposition: form-data; name="filename"; filename="test.data"'\
            '\r\n{data}\r\n'.format(data=content, boundary=boundary)

    body += '--{boundary}--\r\n'.format(boundary=boundary)
    content_type = "multipart/form-data; boundary={}".format(boundary)

    return body, content_type


class TestFileServer(unittest.TestCase):

    def test_tftp(self):
        # Just starting the server performs a copy for validation
        with FileServer(protocol='tftp', subnet='127.0.0.1/32') as fs:
            self.assertEqual(fs['address'], '127.0.0.1')
            self.assertNotEqual(fs['port'], 0)
            self.assertEqual(fs['path'], '/')
            self.assertEqual(fs['protocol'], 'tftp')

    def test_ftp(self):
        with FileServer(protocol='ftp', subnet='127.0.0.1/32') as fs:
            self.assertEqual(fs['address'], '127.0.0.1')
            self.assertNotEqual(fs['port'], 0)
            self.assertEqual(fs['path'], '/')
            self.assertEqual(fs['protocol'], 'ftp')
            self.assertIsInstance(fs['credentials']['ftp']['password'],
                                  SecretString)

    def test_ftp_pass_args(self):
        with tempfile.TemporaryDirectory() as td:
            with FileServer(protocol='ftp',
                            subnet='127.0.0.1',
                            credentials={
                                'ftp': {
                                    'username': 'myuser',
                                    'password': 'mypass'}},
                            path=td) as fs:
                self.assertEqual(fs['address'], '127.0.0.1')
                self.assertEqual(fs['subnet'], '127.0.0.1')
                self.assertEqual(fs['path'], td)
                self.assertEqual(fs['protocol'], 'ftp')
                self.assertIsInstance(fs['credentials']['ftp']['password'],
                                      SecretString)
                self.assertEqual(
                    to_plaintext(fs['credentials']['ftp']['password']),
                    'mypass')

    def test_scp(self):
        with FileServer(protocol='scp', subnet='127.0.0.1/32') as fs:
            self.assertEqual(fs['address'], '127.0.0.1')
            self.assertNotIn('port', fs)
            self.assertNotIn('path', fs)
            self.assertEqual(fs['protocol'], 'scp')

    def test_add_to_testbed(self):
        testbed = AttrDict(servers=AttrDict())
        with FileServer(protocol='ftp',
                        subnet='127.0.0.1/32',
                        testbed=testbed,
                        name='myserver') as fs:
            self.assertEqual(testbed.servers.myserver, fs)

    def test_http(self):
        with FileServer(protocol='http', subnet='127.0.0.1/32') as fs:
            self.assertEqual(fs['address'], '127.0.0.1')
            self.assertIn('port', fs)
            self.assertEqual(fs['path'], '/')
            self.assertEqual(fs['protocol'], 'http')

    def test_http_server_logging(self):
        with self.assertLogs('genie.libs.filetransferutils.fileserver.server') as cm:
            with FileServer(protocol='http', subnet='127.0.0.1/32') as fs:
                self.assertEqual(fs['address'], '127.0.0.1')
                self.assertIn('port', fs)
                self.assertEqual(fs['path'], '/')
                self.assertEqual(fs['protocol'], 'http')
                port = fs['port']
                assert 'INFO:genie.libs.filetransferutils.fileserver.server:'
                f'HTTP File Server started on 127.0.0.1:{port} with path /' in cm.output

    def test_http_auth(self):
        with FileServer(protocol='http',
                        subnet='127.0.0.1/32',
                        custom=dict(http_auth=True),
                        credentials=dict(http=dict(
                            username='test',
                            password='test123'
                        ))
                        ) as fs:
            self.assertEqual(fs['address'], '127.0.0.1')
            self.assertIn('port', fs)
            self.assertEqual(fs['path'], '/')
            self.assertEqual(fs['protocol'], 'http')
            self.assertEqual(fs['credentials']['http']['username'], 'test')
            self.assertEqual(
                to_plaintext(fs['credentials']['http']['password']), 'test123')

    def test_http_multipart_single(self):
        with tempfile.TemporaryDirectory() as td:
            with FileServer(protocol='http', subnet='127.0.0.1/32', path=td) as fs:
                url = 'http://{u}:{p}@localhost:{port}/test.txt'.format(
                    port = fs['port'],
                    u = fs['credentials']['http']['username'],
                    p = to_plaintext(fs['credentials']['http']['password'])
                )
                orig_data = 'test123'
                data, content_type = encode_multipart_formdata(orig_data)
                r = requests.post(url, data=data, headers={'Content-type': content_type})
                self.assertEqual(r.status_code, 201)
                with open(os.path.join(td, 'test.txt'), 'rb') as f:
                    test_data = f.read().decode()
                self.assertEqual(test_data, orig_data)

    def test_http_multipart_multi(self):
        with tempfile.TemporaryDirectory() as td:
            with FileServer(protocol='http', subnet='127.0.0.1/32', path=td) as fs:
                url = 'http://{u}:{p}@localhost:{port}/test.txt'.format(
                    port = fs['port'],
                    u = fs['credentials']['http']['username'],
                    p = to_plaintext(fs['credentials']['http']['password'])
                )
                orig_data = ['test123'] * 2
                data, content_type = encode_multipart_formdata(orig_data)
                r = requests.post(url, data=data, headers={'Content-type': content_type})
                self.assertEqual(r.status_code, 201)
                with open(os.path.join(td, 'test_1.txt'), 'rb') as f:
                    test_data = f.read().decode()
                self.assertEqual(test_data, orig_data[1])
