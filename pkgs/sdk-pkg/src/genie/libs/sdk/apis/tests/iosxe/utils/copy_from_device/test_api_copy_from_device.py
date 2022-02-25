import re
import tempfile
import unittest
from unittest.mock import Mock
from pyats.topology import loader
from genie.libs.sdk.apis.utils import copy_from_device
from genie.libs.filetransferutils import FileServer

import unicon
from unicon.plugins.tests.mock.mock_device_iosxe import MockDeviceTcpWrapperIOSXE

unicon.settings.Settings.POST_DISCONNECT_WAIT_SEC = 0
unicon.settings.Settings.GRACEFUL_DISCONNECT_WAIT_SEC = 0.2


class TestCopyFromDevice(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.md = MockDeviceTcpWrapperIOSXE(hostname='R1', port=0, state='general_enable')
        self.md.start()
        testbed = """
        testbed:
          servers:
            http:
              dynamic: true
              protocol: http
            ftp:
              dynamic: true
              protocol: ftp
            tftp:
              dynamic: true
              protocol: tftp
        devices:
          R1:
            os: iosxe
            type: router
            tacacs:
                username: cisco
            passwords:
                tacacs: cisco
            connections:
              defaults:
                class: unicon.Unicon
              a:
                protocol: telnet
                ip: 127.0.0.1
                port: {}
        """.format(self.md.ports[0])

        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1']
        self.device.connect(mit=True)

    @classmethod
    def tearDownClass(self):
        self.device.disconnect()
        self.md.stop()

    def test_copy_from_device(self):
        self.device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.1']))
        self.device.execute = Mock()
        copy_from_device(self.device, 'test.txt')

        assert re.search(r'copy test.txt http://\w+:\w+@127.0.0.1:\d+/R1_test.txt', str(self.device.execute.call_args))

    def test_copy_from_device_http_server(self):
        self.device.execute = Mock()
        copy_from_device(self.device, 'test.txt', server='http')
        assert re.search(r'copy test.txt http://127.0.0.1/test.txt', str(self.device.execute.call_args))

    def test_copy_from_device_ftp_server(self):
        self.device.execute = Mock()
        copy_from_device(self.device, 'test.txt', server='ftp')
        assert re.search(r'copy test.txt ftp://127.0.0.1/test.txt', str(self.device.execute.call_args))

    def test_copy_from_device_tftp_server(self):
        self.device.execute = Mock()
        copy_from_device(self.device, 'test.txt', remote_path='/tmp', server='tftp')
        assert re.search(r'copy test.txt tftp://127.0.0.1//tmp/test.txt', str(self.device.execute.call_args))

    def test_copy_from_device_tftp_server_1(self):
        self.device.execute = Mock()
        copy_from_device(self.device, 'test.gz.tar', remote_path='/tmp', server='tftp')
        assert re.search(r'copy test.gz.tar tftp://127.0.0.1//tmp/test.gz.tar', str(self.device.execute.call_args))

    def test_copy_from_device_context_manager_http_server(self):
        with tempfile.TemporaryDirectory() as td:
            with FileServer(protocol='http',
                            path=td,
                            testbed=self.testbed,
                            name='mycontextserver'):
                self.device.execute = Mock()
                self.device.api.copy_from_device(protocol='http',
                                                server='mycontextserver',
                                                remote_path='test.txt',
                                                local_path='test.txt')
            assert re.search(r'copy test.txt http://\w+:\w+@127.0.0.1:\d+/test.txt', str(self.device.execute.call_args))

    def test_copy_from_device_context_manager_ftp_server(self):
        with tempfile.TemporaryDirectory() as td:
            with FileServer(protocol='ftp',
                            path=td,
                            testbed=self.testbed,
                            name='mycontextserver'):
                self.device.execute = Mock()
                self.device.api.copy_from_device(protocol='ftp',
                                                server='mycontextserver',
                                                remote_path='test.txt',
                                                local_path='test.txt')
            assert re.search(r'copy test.txt ftp://\w+:\w+@127.0.0.1:\d+/test.txt', str(self.device.execute.call_args))

    def test_copy_from_device_context_manager_tftp_server(self):
        with tempfile.TemporaryDirectory() as td:
            with FileServer(protocol='tftp',
                            path=td,
                            testbed=self.testbed,
                            name='mycontextserver'):
                self.device.execute = Mock()
                self.device.api.copy_from_device(protocol='tftp',
                                                server='mycontextserver',
                                                remote_path='test.txt',
                                                local_path='test.txt')
            assert re.search(r'copy test.txt tftp://127.0.0.1:\d+/test.txt', str(self.device.execute.call_args))
