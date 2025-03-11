
import re
import unittest
from unittest.mock import MagicMock, Mock, call, patch

from ats.topology import Device
from unittest import mock

from genie.libs.clean.stages.tests.utils import create_test_device
from genie.libs.sdk.apis.utils import (
    modify_filename, copy_from_device, copy_to_device, device_recovery_boot,
    configure_management_console, configure_peripheral_terminal_server,
    time_to_int)


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
        device.via = 'telnet'
        device.connections = {}
        device.connections[device.via] = {}
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.1']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.api.convert_server_to_linux_device = Mock(return_value=None)
        device.execute = Mock()
        copy_from_device(device, local_path='flash:test.txt')
        assert re.search(r'copy flash:test.txt http://\w+:\w+@127.0.0.1:\d+/router_test.txt', str(device.execute.call_args))

    def test_copy_from_device_via_proxy(self):
        device = MagicMock()
        device.hostname = 'router'
        device.os = 'iosxe'
        device.via = 'cli'
        device.connections['cli'].get = Mock(return_value='js')
        device.testbed.devices = {}
        device.testbed.devices['js'] = MagicMock()
        device.testbed.devices['js'].api.socat_relay = Mock(return_value=2000)
        device.testbed.devices['js'].api.get_local_ip = Mock(return_value='127.0.0.1')
        device.testbed.devices['js'].execute = Mock(return_value='inet 127.0.0.2')
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.2']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.api.convert_server_to_linux_device = Mock(return_value=None)
        device.execute = Mock()
        copy_from_device(device, local_path='flash:test.txt')
        assert re.search(r'copy flash:test.txt http://\w+:\w+@127.0.0.2:2000/router_test.txt', str(device.execute.call_args))

    def test_copy_from_device_via_testbed_servers_proxy(self):
        device = MagicMock()
        device.hostname = 'router'
        device.os = 'iosxe'
        device.via = 'cli'
        device.connections = {}
        device.connections['cli'] = {}
        device.connections['cli']['proxy'] = 'proxy'
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.2']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.execute = Mock()
        server = MagicMock()
        server.api.socat_relay = Mock(return_value=2000)
        server.api.get_local_ip = Mock(return_value='127.0.0.1')
        server.execute = Mock(return_value='inet 127.0.0.2')
        device.testbed.servers = {}
        device.testbed.servers['proxy'] = {}
        device.api.convert_server_to_linux_device = Mock(return_value=server)
        copy_from_device(device, local_path='flash:test.txt')
        assert re.search(r'copy flash:test.txt http://\w+:\w+@127.0.0.2:2000/router_test.txt', str(device.execute.call_args))

    def test_copy_to_device(self):
        device = MagicMock()
        device.os = 'iosxe'
        device.via = 'cli'
        device.connections = {}
        device.connections[device.via] = {}
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.1']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.api.convert_server_to_linux_device = Mock(return_value=None)
        device.execute = Mock()
        copy_to_device(device, remote_path='/tmp/test.txt')
        assert re.search(r'copy http://\w+:\w+@127.0.0.1:\d+/test.txt flash:', str(device.execute.call_args))

    def test_copy_to_device_via_proxy(self):
        device = MagicMock()
        device.is_ha = False
        device.os = 'iosxe'
        device.via = 'cli'
        device_1 = MagicMock()
        device.connections['cli'].get = Mock(return_value='js')
        device.testbed.devices = {'js':device_1}
        device_1.api.socat_relay = Mock(return_value=2000)
        device_1.api.get_local_ip  = Mock(return_value='127.0.0.1')
        device_1.execute = Mock(return_value='inet 127.0.0.2')
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.2']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.api.convert_server_to_linux_device = Mock(return_value=None)
        device.execute = Mock()
        copy_to_device(device, remote_path='/tmp/test.txt')
        assert re.search(r'copy http://\w+:\w+@127.0.0.2:2000/test.txt flash:', str(device.execute.call_args))

    def test_copy_to_device_via_proxy_ha(self):
        device = MagicMock()
        device.is_ha = True
        device.os = 'iosxe'
        device.active.via ='cli'
        device_1 = MagicMock()
        device.connections['cli'].get = Mock(return_value='js')
        device.testbed.devices = {'js':device_1}
        device_1.api.socat_relay = Mock(return_value=2000)
        device_1.api.get_local_ip  = Mock(return_value='127.0.0.1')
        device_1.execute = Mock(return_value='inet 127.0.0.2')
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.2']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.api.convert_server_to_linux_device = Mock(return_value=None)
        device.execute = Mock()
        copy_to_device(device, remote_path='/tmp/test.txt')
        assert re.search(r'copy http://\w+:\w+@127.0.0.2:2000/test.txt flash:', str(device.execute.call_args))

    def test_copy_to_device_via_testbed_servers_proxy(self):
        device = MagicMock()
        device.hostname = 'router'
        device.os = 'iosxe'
        device.via = 'cli'
        device.connections = {}
        device.connections['cli'] = {}
        device.connections['cli']['proxy'] = 'proxy'
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.2']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.execute = Mock()
        server = MagicMock()
        server.api.socat_relay = Mock(return_value=2000)
        server.api.get_local_ip = Mock(return_value='127.0.0.1')
        server.execute = Mock(return_value='inet 127.0.0.2')
        device.testbed.servers = Mock(return_value=server)
        device.testbed.servers = {}
        device.testbed.servers['proxy'] = {}
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

    def test_configure_management_console(self):
        dev1 = MagicMock()
        terminal_device_1 =  MagicMock()
        terminal_device_1.is_connected.side_effect =[False, True, True, True]
        dev1.api.configure_terminal_line_speed = MagicMock()
        dev1.parse.return_value = {'baud_rate':{'tx':115200}}
        dev1.connect = MagicMock()
        dev1.connect.side_effect = [Exception, Exception, True]
        dev1.peripherals = {'terminal_server': {'terminal_1': [{'line': 14}]}}
        dev1.testbed.devices = {'terminal_1':terminal_device_1}
        configure_management_console(dev1)
        expected_calls = [
            call(terminal_device_1, 14, 9600),
            call(terminal_device_1, 14, 115200)]
        self.assertEqual(dev1.api.configure_terminal_line_speed.mock_calls, expected_calls)

        dev2 = MagicMock()
        terminal_device_2 =  MagicMock()
        terminal_device_2.is_connected.side_effect =[False, True, True, True]
        dev2.connect = MagicMock()
        dev2.api.configure_terminal_line_speed = MagicMock()
        dev2.connect.side_effect = [Exception, Exception, True]
        dev2.peripherals = {'terminal_server': {'terminal_2': [{'line': 14, 'speed': 9600}, {'line': 15, 'speed': 9600}]}}
        dev1.parse.return_value = {'baud_rate':{'tx':115200}}
        dev2.testbed.devices = {'terminal_2':terminal_device_2}
        dev2.state_machine.current_state = 'enable'
        configure_management_console(dev2)
        expected_calls = [
            call(terminal_device_2, 14, 9600),
            call(terminal_device_2, 15, 9600),
            call(terminal_device_2, 14, 115200),
            call(terminal_device_2, 15, 115200),
            call(terminal_device_2, 14, 9600),
            call(terminal_device_2, 15, 9600),]
        self.assertEqual(dev2.api.configure_terminal_line_speed.mock_calls, expected_calls)

        dev3 = MagicMock()
        terminal_device_3 =  MagicMock()
        terminal_device_3.is_connected.side_effect =[False, True]
        dev3.connect = MagicMock()
        dev3.connect.side_effect = [True]
        dev3.api.configure_terminal_line_speed = MagicMock()
        dev3.parse.return_value = {'baud_rate':{'tx':19200}}
        dev3.peripherals = {'terminal_server': {'terminal_3': [{'line': 14, 'speed': 9600}]}}
        dev3.testbed.devices = {'terminal_3':terminal_device_3}
        dev3.state_machine.current_state = 'enable'
        configure_management_console(dev3)
        expected_calls = [
            call(terminal_device_3,14, 9600)]
        self.assertEqual(dev3.api.configure_terminal_line_speed.mock_calls, expected_calls)

        dev4 = MagicMock()
        terminal_device_4 =  MagicMock()
        terminal_device_4.is_connected.side_effect =[False, True, True, True]
        terminal_device_5 =  MagicMock()
        terminal_device_5.is_connected.side_effect =[False, True, True, True]
        dev4.connect = MagicMock()
        dev4.connect.side_effect = [Exception, Exception, True]
        dev4.parse.return_value = {'baud_rate':{'tx':19200}}
        dev4.api.configure_terminal_line_speed = MagicMock()
        dev4.peripherals = {'terminal_server': {'terminal_4': [{'line': 14, 'speed': 9600}],
                                                'terminal_5': [{'line': 15, 'speed': 9600}]}}
        dev4.testbed.devices = {'terminal_4':terminal_device_4, 'terminal_5':terminal_device_5 }
        dev4.state_machine.current_state = 'enable'
        configure_management_console(dev4)
        expected_calls = [
            call(terminal_device_4, 14, 9600),
            call(terminal_device_5, 15, 9600),
            call(terminal_device_4, 14, 115200),
            call(terminal_device_5, 15, 115200),
            call(terminal_device_4, 14, 9600),
            call(terminal_device_5, 15, 9600,)]
        self.assertEqual(dev4.api.configure_terminal_line_speed.mock_calls, expected_calls)

    def test_configure_peripheral_terminal_server(self):
        dev1 = MagicMock()
        dev1.os = 'iosxe'
        terminal_device =  MagicMock()
        terminal_device.configure = MagicMock()
        terminal_device.connections = {'cli': MagicMock}
        dev1.peripherals = {'terminal_server': {'terminal_1': [{'line': 14, 'speed': 9600}, {'line': 15, 'speed': 9600}]}}
        dev1.testbed.devices = {'terminal_1':terminal_device}
        configure_peripheral_terminal_server(dev1)

        expected_calls = [
            call(['line 14', 'speed 9600']),
            call(['line 15', 'speed 9600'])]

        self.assertEqual(terminal_device.configure.mock_calls, expected_calls)

        dev2 = MagicMock()
        dev2.os = 'iosxe'
        terminal_device =  MagicMock()
        terminal_device.configure = MagicMock()
        terminal_device.connections = {'cli': MagicMock}
        dev2.peripherals = {'terminal_server':[14,15]}
        dev2.testbed.devices = {'terminal_1':terminal_device}
        configure_peripheral_terminal_server(dev1)

        terminal_device.configure.assert_not_called()

def test_time_to_int(self):
        time = '10:58'
        result = time_to_int(time)
        self.assertEqual(result, 658)

        time = '10:20:30'
        result = time_to_int(time)
        self.assertEqual(result, 37230)

        time = '6d14h'
        result = time_to_int(time)
        self.assertEqual(result, 568800)