
import re
import unittest
from unittest.mock import MagicMock, Mock, call, patch

from ats.topology import Device

from genie.libs.clean.stages.tests.utils import create_test_device
from genie.libs.sdk.apis.utils import (
    modify_filename, copy_from_device, copy_to_device, device_recovery_boot)


class TestUtilsApi(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'

    def test_modify_filename_exceed(self):
        truncated = modify_filename(device=self.device,
                                    file='Lorem_ipsum_dolor_sit_amet_consectetur_adipiscing_elit.bin',
                                    directory='/tftp_boot/bla',
                                    protocol='ftp',
                                    server='111.111.111.111',
                                    check_image_length=True,
                                    limit=63)
        self.assertEqual(truncated, 'Lorem_ipsum_dolor_sit_.bin')

    def test_modify_filename_same(self):
        original = 'Lorem_ipsum.bin'
        truncated = modify_filename(device=self.device,
                                    file=original,
                                    directory='/tftp_boot/bla/',
                                    protocol='ftp',
                                    server='111.111.111.111', limit=63)
        self.assertEqual(truncated, original)

    def test_copy_from_device(self):
        device = MagicMock()
        device.hostname = 'router'
        device.os = 'iosxe'
        device.api = MagicMock()
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.1']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.execute = Mock()
        copy_from_device(device, local_path='flash:test.txt')
        assert re.search(r'copy flash:test.txt http://\w+:\w+@127.0.0.1:\d+/router_test.txt', str(device.execute.call_args))

    def test_copy_from_device_via_proxy(self):
        device = MagicMock()
        device.hostname = 'router'
        device.os = 'iosxe'
        device.via = 'cli'
        device.connections['cli'].get = Mock(return_value='js')
        device.testbed.devices['js'].api.socat_relay = Mock(return_value=2000)
        device.testbed.devices['js'].execute = Mock(return_value='inet 127.0.0.2')
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.2']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.execute = Mock()
        copy_from_device(device, local_path='flash:test.txt')
        assert re.search(r'copy flash:test.txt http://\w+:\w+@127.0.0.2:2000/router_test.txt', str(device.execute.call_args))

    def test_copy_from_device_via_testbed_servers_proxy(self):
        device = MagicMock()
        device.hostname = 'router'
        device.os = 'iosxe'
        device.via = 'cli'
        device.connections['cli'].get = Mock(return_value={})
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.2']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        server = MagicMock()
        server.api.socat_relay = Mock(return_value=2000)
        server.execute = Mock(return_value='inet 127.0.0.2')
        device.testbed.servers = Mock(return_value=server)
        device.api.convert_server_to_linux_device = Mock(return_value=server)
        copy_from_device(device, local_path='flash:test.txt')
        assert re.search(r'copy flash:test.txt http://\w+:\w+@127.0.0.2:2000/router_test.txt', str(device.execute.call_args))

    def test_copy_to_device(self):
        device = MagicMock()
        device.os = 'iosxe'
        device.via = 'cli'
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.1']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.execute = Mock()
        copy_to_device(device, remote_path='/tmp/test.txt')
        assert re.search(r'copy http://\w+:\w+@127.0.0.1:\d+/test.txt flash:', str(device.execute.call_args))

    def test_copy_to_device_via_proxy(self):
        device = MagicMock()
        device.os = 'iosxe'
        device.via = 'cli'
        device.connections['cli'].get = Mock(return_value='js')
        device.testbed.devices['js'].api.socat_relay = Mock(return_value=2000)
        device.testbed.devices['js'].execute = Mock(return_value='inet 127.0.0.2')
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.2']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.execute = Mock()
        copy_to_device(device, remote_path='/tmp/test.txt')
        assert re.search(r'copy http://\w+:\w+@127.0.0.2:2000/test.txt flash:', str(device.execute.call_args))

    def test_copy_to_device_via_testbed_servers_proxy(self):
        device = MagicMock()
        device.hostname = 'router'
        device.os = 'iosxe'
        device.via = 'cli'
        device.connections['cli'].get = Mock(return_value={})
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.2']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        server = MagicMock()
        server.api.socat_relay = Mock(return_value=2000)
        server.execute = Mock(return_value='inet 127.0.0.2')
        device.testbed.servers = Mock(return_value=server)
        device.api.convert_server_to_linux_device = Mock(return_value=server)
        copy_to_device(device, remote_path='/tmp/test.txt')
        assert re.search(r'copy http://\w+:\w+@127.0.0.2:2000/test.txt flash:', str(device.execute.call_args))

    def test_device_recovery_boot(self):
        device = create_test_device(name='aDevice', os='iosxe')
        device.destroy = Mock()
        device.start = 'telnet 127.0.0.1 0000'
        device.instantiate = Mock()
        device.is_ha = False
        device.clean = {'device_recovery':
                            {'golden_image':'bootflash:packages.conf',
                            'recovery_password':'lab'}}
        with patch("genie.libs.sdk.apis.utils.pcall") as pcall_mock:
            device_recovery_boot(device)
            pcall_mock.assert_called_once()