#!/usr/bin/env python

import tempfile
import unittest
from unittest.mock import Mock

from genie.libs.filetransferutils import FileServer
from pyats.datastructures import AttrDict
from pyats.utils.secret_strings import SecretString, to_plaintext


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

    def test_http_auth(self):
        with FileServer(protocol='http',
                        subnet='127.0.0.1/32',
                        http_auth=True,
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
