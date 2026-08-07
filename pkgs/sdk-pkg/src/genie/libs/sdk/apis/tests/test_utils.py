
import re
import unittest
from ipaddress import IPv4Interface
from textwrap import dedent
from unittest.mock import MagicMock, Mock, call, patch, PropertyMock


from ats.topology import Device
from unittest import mock

from genie.libs.clean.stages.tests.utils import create_test_device
from genie.libs.sdk.apis.utils import (
    modify_filename, copy_from_device, copy_to_device, device_recovery_boot,
    configure_management_console, configure_peripheral_terminal_server,
    time_to_int, slugify_filename, get_file_size_from_server,
    get_interface_from_yaml, convert_server_to_linux_device, get_proxy,
    _management_session_uses_gateway, _infer_management_gateway_addresses)


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
        device.api.get_proxy = Mock(return_value=None)
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.1']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.api.convert_server_to_linux_device = Mock(return_value=None)
        device.execute = Mock()
        copy_from_device(device, local_path='flash:test.txt', protocol='http')
        assert re.search(r'copy flash:test.txt http://\w+:\w+@127.0.0.1:\d+/router_test.txt', str(device.execute.call_args))

    def test_copy_from_device_session_source_is_gateway(self):
        device = MagicMock()
        device.hostname = 'router'
        device.os = 'iosxe'
        device.management = {'gateway': {'ipv4': '192.168.122.1'}}
        device.api.get_proxy = Mock(return_value=None)
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(
            return_value=('192.168.122.77', ['192.168.122.1']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.execute = Mock()

        with patch('genie.libs.sdk.apis.utils.log.info') as log_info:
            copy_from_device(
                device, local_path='flash:test.txt', protocol='http')

        log_info.assert_any_call(
            'Management session source IP %s matches configured management '
            'gateway; using local IP for dynamic file server',
            '192.168.122.1')

        assert re.search(
            r'copy flash:test.txt http://\w+:\w+@127.0.0.1:\d+/router_test.txt',
            str(device.execute.call_args))

    def test_copy_from_device_session_source_looks_like_gateway_without_testbed_gateway(self):
        device = MagicMock()
        device.hostname = 'router'
        device.os = 'iosxe'
        # No configured gateway, but a management address with a reliable /24
        # prefix so the gateway can be inferred from the configured subnet.
        device.management = {
            'address': {'ipv4': IPv4Interface('192.168.122.77/24')}}
        device.api.get_proxy = Mock(return_value=None)
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(
            return_value=('192.168.122.77', ['192.168.122.1']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.execute = Mock()

        with patch('genie.libs.sdk.apis.utils.log.info') as log_info:
            copy_from_device(
                device, local_path='flash:test.txt', protocol='http')

        log_info.assert_any_call(
            'Management session source IP %s appears to be a gateway for '
            'management IP %s; using local IP for dynamic file server',
            '192.168.122.1', '192.168.122.77')

        assert re.search(
            r'copy flash:test.txt http://\w+:\w+@127.0.0.1:\d+/router_test.txt',
            str(device.execute.call_args))

    def test_copy_from_device_via_proxy(self):
        device = MagicMock()
        device.hostname = 'router'
        device.os = 'iosxe'
        device.via = 'cli'
        device.connections['cli'] = Mock()
        device.connections['cli'].get = Mock(return_value='js')
        device.testbed.devices = {}
        device.testbed.devices['js'] = MagicMock()
        device.testbed.devices['js'].api.socat_relay = Mock(return_value=2000)
        device.testbed.devices['js'].api.get_local_ip = Mock(return_value='127.0.0.1')
        device.testbed.devices['js'].execute = Mock(return_value='inet 127.0.0.2')
        device.api.get_proxy = Mock(return_value='js')
        device.testbed.devices['js'].api.get_route_iface_source_ip = Mock(return_value=(None, '127.0.0.2'))
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.2']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.api.convert_server_to_linux_device = Mock(return_value=None)
        device.execute = Mock()
        copy_from_device(device, local_path='flash:test.txt', protocol='http')
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
        server.api.get_route_iface_source_ip = Mock(return_value=(None, '127.0.0.2'))
        device.testbed.servers = {}
        device.testbed.servers['proxy'] = {}
        device.api.convert_server_to_linux_device = Mock(return_value=server)
        copy_from_device(device, local_path='flash:test.txt', protocol='http')
        assert re.search(r'copy flash:test.txt http://\w+:\w+@127.0.0.2:2000/router_test.txt', str(device.execute.call_args))

    def test_convert_server_to_linux_device_missing_server_block(self):
        device = MagicMock()
        device.testbed = object()
        fileutils = MagicMock()
        fileutils.get_server_block.return_value = None
        fileutils.get_hostname.return_value = 'server.example.com'

        with patch('genie.libs.sdk.apis.utils.FileUtils') as fileutils_cls, \
                patch('genie.libs.sdk.apis.utils.Device') as device_cls:
            fileutils_cls.return_value.__enter__.return_value = fileutils

            result = convert_server_to_linux_device(device, 'fileserver')

        self.assertIsNone(result)
        fileutils_cls.assert_called_once_with(testbed=device.testbed)
        fileutils.get_server_block.assert_called_once_with('fileserver')
        fileutils.get_hostname.assert_called_once_with('fileserver')
        device_cls.assert_not_called()

    def test_get_proxy_without_via_metadata(self):
        device = type('DeviceMock', (), {})()
        device.connections = {
            'defaults': {'proxy': 'ignored'},
            'cli': {'proxy': 'proxy-host'},
        }

        self.assertEqual(get_proxy(device), 'proxy-host')

    def test_copy_to_device(self):
        device = MagicMock()
        device.os = 'iosxe'
        device.via = 'cli'
        device.connections = {}
        device.connections[device.via] = {}
        device.api.get_proxy = Mock(return_value=None)
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(return_value=('127.0.0.1', ['127.0.0.1']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.api.convert_server_to_linux_device = Mock(return_value=None)
        device.execute = Mock()
        copy_to_device(device, remote_path='/tmp/test.txt', protocol='http')
        assert re.search(r'copy http://\w+:\w+@127.0.0.1:\d+/test.txt flash:', str(device.execute.call_args))

    def test_copy_to_device_via_proxy(self):
        device = MagicMock()
        device.is_ha = False
        device.os = 'iosxe'
        device.via = 'cli'
        device_1 = MagicMock()
        device.connections['cli'] = Mock()
        device.connections['cli'].get = Mock(return_value='js')
        device.testbed.devices = {'js':device_1}
        device.api.get_proxy = Mock(return_value='js')
        device_1.api.socat_relay = Mock(return_value=2000)
        device_1.api.get_local_ip  = Mock(return_value='127.0.0.1')
        device_1.execute = Mock(return_value='inet 127.0.0.2')
        device_1.api.get_route_iface_source_ip = Mock(return_value=(None, '127.0.0.2'))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.api.convert_server_to_linux_device = Mock(return_value=None)
        device.execute = Mock()
        copy_to_device(device, remote_path='/tmp/test.txt', protocol='http')
        assert re.search(r'copy http://\w+:\w+@127.0.0.2:2000/test.txt flash:', str(device.execute.call_args))

    def test_copy_to_device_via_proxy_ha(self):
        device = MagicMock()
        device.is_ha = True
        device.os = 'iosxe'
        device.active.via ='cli'
        device_1 = MagicMock()
        device.connections['cli'].get = Mock(return_value='js')
        device.testbed.devices = {'js':device_1}
        device.api.get_proxy = Mock(return_value='js')
        device_1.api.socat_relay = Mock(return_value=2000)
        device_1.api.get_local_ip  = Mock(return_value='127.0.0.1')
        device_1.execute = Mock(return_value='inet 127.0.0.2')
        device_1.api.get_route_iface_source_ip = Mock(return_value=(None, '127.0.0.2'))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.api.convert_server_to_linux_device = Mock(return_value=None)
        device.execute = Mock()
        copy_to_device(device, remote_path='/tmp/test.txt', protocol='http')
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
        server.api.get_route_iface_source_ip = Mock(return_value=(None, '127.0.0.2'))
        device.testbed.servers = Mock(return_value=server)
        device.testbed.servers = {}
        device.testbed.servers['proxy'] = {}
        device.api.convert_server_to_linux_device = Mock(return_value=server)
        copy_to_device(device, remote_path='/tmp/test.txt', protocol='http')
        assert re.search(r'copy http://\w+:\w+@127.0.0.2:2000/test.txt flash:', str(device.execute.call_args))

    def test_copy_to_device_session_source_is_gateway(self):
        device = MagicMock()
        device.os = 'iosxe'
        device.management = {'gateway': {'ipv4': '192.168.122.1'}}
        device.api.get_proxy = Mock(return_value=None)
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(
            return_value=('192.168.122.77', ['192.168.122.1']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.execute = Mock()

        copy_to_device(device, remote_path='/tmp/test.txt', protocol='http')

        assert re.search(
            r'copy http://\w+:\w+@127.0.0.1:\d+/test.txt flash:',
            str(device.execute.call_args))

    def test_copy_to_device_session_source_looks_like_gateway_without_testbed_gateway(self):
        device = MagicMock()
        device.os = 'iosxe'
        # No configured gateway, but a management address with a reliable /24
        # prefix so the gateway can be inferred from the configured subnet.
        device.management = {
            'address': {'ipv4': IPv4Interface('192.168.122.77/24')}}
        device.api.get_proxy = Mock(return_value=None)
        device.api.get_mgmt_ip_and_mgmt_src_ip_addresses = Mock(
            return_value=('192.168.122.77', ['192.168.122.1']))
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.execute = Mock()

        copy_to_device(device, remote_path='/tmp/test.txt', protocol='http')

        assert re.search(
            r'copy http://\w+:\w+@127.0.0.1:\d+/test.txt flash:',
            str(device.execute.call_args))

    def test_get_file_size_from_server_via_proxy(self):
        device = MagicMock()
        device.api = MagicMock()
        device.api.get_proxy = Mock(return_value='js')
        device.api.convert_server_to_linux_device = Mock(return_value=None)

        proxy_dev = MagicMock()
        proxy_dev.connect = Mock()
        proxy_dev.api.start_socat_relay = Mock(return_value=(2000, '1234'))
        proxy_dev.api.stop_socat_relay = Mock()

        device.testbed.devices = {'js': proxy_dev}

        fu = MagicMock()
        fu.get_hostname = Mock(return_value='proxy.host')
        fu.validate_and_update_url = Mock(return_value='ftp://user:pass@1.1.1.1/path/file.bin')
        stat_result = MagicMock()
        stat_result.st_size = 4321
        fu.stat = Mock(return_value=stat_result)

        size = get_file_size_from_server(device=device,
                                         server='1.1.1.1',
                                         path='path/file.bin',
                                         protocol='ftp',
                                         timeout=10,
                                         fu_session=fu)

        self.assertEqual(size, 4321)
        proxy_dev.api.start_socat_relay.assert_called_once_with(
            remote_ip='1.1.1.1',
            remote_port='21',
            protocol='TCP4')
        fu.stat.assert_called_once_with(
            target='ftp://user:pass@proxy.host:2000/path/file.bin',
            timeout_seconds=10)
        proxy_dev.api.stop_socat_relay.assert_called_once_with('1234')

    def test_get_file_size_from_server_via_proxy_custom_port_http(self):
        device = MagicMock()
        device.api = MagicMock()
        device.api.get_proxy = Mock(return_value='js')
        device.api.convert_server_to_linux_device = Mock(return_value=None)
        proxy_dev = MagicMock()
        proxy_dev.connect = Mock()
        proxy_dev.api.start_socat_relay = Mock(return_value=(2000, '1234'))
        proxy_dev.api.stop_socat_relay = Mock()

        device.testbed.devices = {'js': proxy_dev}

        fu = MagicMock()
        fu.get_hostname = Mock(return_value='proxy.host')
        fu.validate_and_update_url = Mock(
            return_value='http://user:pass@10.0.0.1:8080/path/file.bin')
        stat_result = MagicMock()
        stat_result.st_size = 4321
        fu.stat = Mock(return_value=stat_result)

        size = get_file_size_from_server(device=device,
                                         server='myhttpserver',
                                         path='path/file.bin',
                                         protocol='http',
                                         timeout=10,
                                         fu_session=fu)

        self.assertEqual(size, 4321)
        proxy_dev.api.start_socat_relay.assert_called_once_with(
            remote_ip='10.0.0.1',
            remote_port='8080',
            protocol='TCP4')
        fu.stat.assert_called_once_with(
            target='http://user:pass@proxy.host:2000/path/file.bin',
            timeout_seconds=10)
        proxy_dev.api.stop_socat_relay.assert_called_once_with('1234')

    def test_get_file_size_from_server_via_proxy_stops_relay_on_error(self):
        device = MagicMock()
        device.api = MagicMock()
        device.api.get_proxy = Mock(return_value='js')
        device.api.convert_server_to_linux_device = Mock(return_value=None)

        proxy_dev = MagicMock()
        proxy_dev.connect = Mock()
        proxy_dev.api.start_socat_relay = Mock(return_value=(2000, '1234'))
        proxy_dev.api.stop_socat_relay = Mock()
        device.testbed.devices = {'js': proxy_dev}

        fu = MagicMock()
        fu.get_hostname = Mock(return_value='proxy.host')
        fu.validate_and_update_url = Mock(return_value='ftp://user:pass@1.1.1.1/path/file.bin')
        fu.stat = Mock(side_effect=FileNotFoundError('missing'))

        with self.assertRaises(FileNotFoundError):
            get_file_size_from_server(device=device,
                                      server='1.1.1.1',
                                      path='path/file.bin',
                                      protocol='ftp',
                                      timeout=10,
                                      fu_session=fu)

        proxy_dev.api.stop_socat_relay.assert_called_once_with('1234')

    def test_device_recovery_boot(self):
        device = create_test_device(name='aDevice', os='iosxe')
        device.destroy = Mock()
        device.start = 'telnet 127.0.0.1 0000'
        device.instantiate = Mock()
        device.is_ha = False
        device.clean = {'device_recovery':
                            {'golden_image':'bootflash:packages.conf',
                            'recovery_password':'lab'}}
        with patch("genie.libs.sdk.apis.utils.Lookup") as lookup_mock:
            lookup_clean = mock.Mock()
            lookup_clean.clean.recovery.recovery.recovery_worker = mock.Mock()
            lookup_mock.from_device.return_value = lookup_clean
            device_recovery_boot(device)
            expected_calls = [call(device=device, console_activity_pattern=None, console_breakboot_char='\x03', console_breakboot_telnet_break=False,
             grub_activity_pattern=None, grub_breakboot_char='c', break_count=15, timeout=750, golden_image='bootflash:packages.conf', tftp_boot={}, recovery_password='lab')]
            lookup_clean.clean.recovery.recovery.recovery_worker.mock_calls
            self.assertEqual(lookup_clean.clean.recovery.recovery.recovery_worker.mock_calls, expected_calls)

    def test_configure_management_console(self):
        dev1 = MagicMock()
        terminal_device_1 =  MagicMock()
        terminal_device_1.is_connected.side_effect =[False, True, True, True]
        dev1.api.configure_terminal_line_speed = MagicMock()
        dev1.parse.return_value = {'baud_rate':{'tx':115200}}
        dev1.connect = MagicMock()
        dev1.spawn = MagicMock()
        dev1.spawn.buffer = '\\x86'

        dev1.connect.side_effect = [Exception, Exception, True]
        dev1.peripherals = {'terminal_server': {'terminal_1': [{'line': 14}]}}
        dev1.testbed.devices = {'terminal_1':terminal_device_1}
        configure_management_console(dev1, max_time=1, check_interval=1)
        expected_calls = [
            call(terminal_device_1, 14, 9600),
            call(terminal_device_1, 14, 115200)]
        self.assertEqual(dev1.api.configure_terminal_line_speed.mock_calls, expected_calls)

        dev2 = MagicMock()
        terminal_device_2 =  MagicMock()
        terminal_device_2.is_connected.side_effect =[False, True, True, True]
        dev2.connect = MagicMock()
        dev2.api.configure_terminal_line_speed = MagicMock()
        dev2.connect.side_effect = [Exception, Exception, True, True]
        dev2.peripherals = {'terminal_server': {'terminal_2': [{'line': 14, 'speed': 9600}, {'line': 15, 'speed': 9600}]}}
        dev2.parse.return_value = {'baud_rate':{'tx':115200}}
        dev2.testbed.devices = {'terminal_2':terminal_device_2}
        dev2.state_machine.current_state = 'enable'
        dev2.spawn.buffer = '\\x86'
        configure_management_console(dev2, max_time=1, check_interval=1)
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
        dev3.connect.side_effect = [True, True]
        dev3.api.configure_terminal_line_speed = MagicMock()
        dev3.parse.return_value = {'baud_rate':{'tx':19200}}
        dev3.peripherals = {'terminal_server': {'terminal_3': [{'line': 14, 'speed': 9600}]}}
        dev3.testbed.devices = {'terminal_3':terminal_device_3}
        dev3.state_machine.current_state = 'enable'
        configure_management_console(dev3, max_time=30, check_interval=10)
        expected_calls = [
            call(terminal_device_3,14, 9600)]
        self.assertEqual(dev3.api.configure_terminal_line_speed.mock_calls, expected_calls)

        dev4 = MagicMock()
        terminal_device_4 =  MagicMock()
        terminal_device_4.is_connected.side_effect =[False, True, True, True, True]
        terminal_device_5 =  MagicMock()
        terminal_device_5.is_connected.side_effect =[False, True, True, True, True]
        dev4.connect = MagicMock()
        dev4.connect.side_effect = [Exception, Exception, True, True]
        dev4.spawn = MagicMock()
        type(dev4.spawn).buffer = PropertyMock(side_effect=['\\x86', '\\xfe', '\\x86', '\\xfe', '\\x86','\\xfe86','Router>'])
        dev4.parse.return_value = {'baud_rate':{'tx':19200}}
        dev4.api.configure_terminal_line_speed = MagicMock()
        dev4.peripherals = {'terminal_server': {'terminal_4': [{'line': 14, 'speed': 9600}],
                                                'terminal_5': [{'line': 15, 'speed': 9600}]}}
        dev4.testbed.devices = {'terminal_4':terminal_device_4, 'terminal_5':terminal_device_5 }
        dev4.state_machine.current_state = 'enable'
        configure_management_console(dev4, max_time=1, check_interval=1)
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
        self.assertEqual(result, 39480)

        time = '10:20:30'
        result = time_to_int(time)
        self.assertEqual(result, 37230)

        time = '6d14h'
        result = time_to_int(time)
        self.assertEqual(result, 568800)

class TestSlugifyFilename(unittest.TestCase):

    def test_slugify_filename_double_suffix_hostname_present(self):
        device = MagicMock()
        device.hostname = "Lime1_GX"

        path = "bootflash:/ctc_Lime1_GX_2025_09_19_active.tar.gz"
        result = slugify_filename(device, path)
        self.assertEqual(result, "ctc_Lime1_GX_2025_09_19_active.tar.gz")


class TestGetInterfaceFromYaml(unittest.TestCase):

    def setUp(self):
        # Sample testbed topology for testing
        self.testbed_topology = {
            'R1': {
                'interfaces': {
                    'GigabitEthernet0/0/0': {
                        'link': 'R1_R2_1',
                        'type': 'ethernet'
                    },
                    'GigabitEthernet0/0/1': {
                        'link': 'R1_R3_1',
                        'type': 'ethernet'
                    },
                    'GigabitEthernet0/0/2': {
                        'link': 'R1_R2_2',
                        'type': 'ethernet'
                    }
                }
            },
            'R2': {
                'interfaces': {
                    'GigabitEthernet0/0/0': {
                        'link': 'R1_R2_1',
                        'type': 'ethernet'
                    },
                    'GigabitEthernet0/0/1': {
                        'link': 'R1_R2_2',
                        'type': 'ethernet'
                    }
                }
            },
            'R3': {
                'interfaces': {
                    'GigabitEthernet0/0/0': {
                        'link': 'R1_R3_1',
                        'type': 'ethernet'
                    }
                }
            }
        }

        # Topology with segments for segment testing
        self.testbed_topology_with_segments = {
            'R1': {
                'interfaces': {
                    'GigabitEthernet0/0/0': {
                        'segment': 'segment1',
                        'link': 'R1_R2_1',  # Add link to prevent alias resolution
                        'type': 'ethernet'
                    },
                    'GigabitEthernet0/0/1': {
                        'segment': 'segment2',
                        'link': 'R1_R2_2',  # Add link to prevent alias resolution
                        'type': 'ethernet'
                    }
                }
            },
            'R2': {
                'interfaces': {
                    'GigabitEthernet0/0/0': {
                        'segment': 'segment1',
                        'link': 'R1_R2_1',
                        'type': 'ethernet'
                    },
                    'GigabitEthernet0/0/1': {
                        'segment': 'segment2',
                        'link': 'R1_R2_2',
                        'type': 'ethernet'
                    }
                }
            },
            # Segment definitions
            'segment1': {
                'type': 'QINQ'
            },
            'segment2': {
                'type': 'QINQ'
            }
        }

    def test_get_interface_with_link_name(self):
        """Test getting interface using specific link name"""
        result = get_interface_from_yaml('R1', 'R2', 'R1_R2_1', self.testbed_topology)
        self.assertEqual(result, 'GigabitEthernet0/0/0')

    def test_get_interface_with_numeric_index(self):
        """Test getting interface using numeric index"""
        # First link (index 0) between R1 and R2
        result = get_interface_from_yaml('R1', 'R2', 0, self.testbed_topology)
        self.assertEqual(result, 'GigabitEthernet0/0/0')

        # Second link (index 1) between R1 and R2
        result = get_interface_from_yaml('R1', 'R2', 1, self.testbed_topology)
        self.assertEqual(result, 'GigabitEthernet0/0/2')

    def test_get_interface_with_string_numeric_index(self):
        """Test getting interface using string numeric index"""
        result = get_interface_from_yaml('R1', 'R2', '0', self.testbed_topology)
        self.assertEqual(result, 'GigabitEthernet0/0/0')

        result = get_interface_from_yaml('R1', 'R2', '1', self.testbed_topology)
        self.assertEqual(result, 'GigabitEthernet0/0/2')

    def test_get_interface_single_link(self):
        """Test getting interface when devices have only one common link"""
        result = get_interface_from_yaml('R1', 'R3', 0, self.testbed_topology)
        self.assertEqual(result, 'GigabitEthernet0/0/1')

        result = get_interface_from_yaml('R1', 'R3', 'R1_R3_1', self.testbed_topology)
        self.assertEqual(result, 'GigabitEthernet0/0/1')

    def test_get_interface_invalid_index_raises_exception(self):
        """Test that invalid index raises appropriate exception"""
        with self.assertRaises(Exception) as context:
            get_interface_from_yaml('R1', 'R2', 5, self.testbed_topology)

        self.assertIn("Link '5' between 'R1' and 'R2' does not exists", str(context.exception))
        self.assertIn("there is only '2' links between them", str(context.exception))

    def test_get_interface_no_common_links_raises_exception(self):
        """Test behavior when no common links exist between devices"""
        # Add a device with no common links
        topology_no_common = self.testbed_topology.copy()
        topology_no_common['R4'] = {
            'interfaces': {
                'GigabitEthernet0/0/0': {
                    'link': 'R4_only_link',
                    'type': 'ethernet'
                }
            }
        }

        with self.assertRaises(Exception) as context:
            get_interface_from_yaml('R1', 'R4', 0, topology_no_common)

        self.assertIn("Link '0' between 'R1' and 'R4' does not exists", str(context.exception))
        self.assertIn("there is only '0' links between them", str(context.exception))

    def test_get_interface_multiple_interfaces_same_link_returns_first(self):
        """Test that multiple interfaces for same link returns the first interface"""
        # Create topology where link maps to multiple interfaces
        topology_multiple = {
            'R1': {
                'interfaces': {
                    'GigabitEthernet0/0/0': {
                        'link': 'R1_R2_1',
                        'type': 'ethernet'
                    },
                    'GigabitEthernet0/0/1': {
                        'link': 'R1_R2_1',  # Same link, different interface
                        'type': 'ethernet'
                    }
                }
            },
            'R2': {
                'interfaces': {
                    'GigabitEthernet0/0/0': {
                        'link': 'R1_R2_1',
                        'type': 'ethernet'
                    }
                }
            }
        }

        # Function should return the first interface it finds
        result = get_interface_from_yaml('R1', 'R2', 'R1_R2_1', topology_multiple)
        self.assertEqual(result, 'GigabitEthernet0/0/0')

    @patch('ast.literal_eval')
    def test_get_interface_with_non_dict_topology(self, mock_literal_eval):
        """Test handling of non-dict testbed_topology parameter"""
        # Mock topology as string that needs parsing
        topology_string = "{'R1': {'interfaces': {'GigabitEthernet0/0/0': {'link': 'R1_R2_1'}}}}"
        mock_literal_eval.return_value = self.testbed_topology

        result = get_interface_from_yaml('R1', 'R2', 0, topology_string)

        # Verify ast.literal_eval was called
        mock_literal_eval.assert_called_once()
        self.assertEqual(result, 'GigabitEthernet0/0/0')

    def test_get_interface_with_kwargs(self):
        """Test that function accepts additional keyword arguments"""
        # Should not raise error even with extra kwargs
        result = get_interface_from_yaml(
            'R1', 'R2', 0, self.testbed_topology,
            extra_param1='value1', extra_param2='value2'
        )
        self.assertEqual(result, 'GigabitEthernet0/0/0')

    def test_get_interface_case_sensitivity(self):
        """Test that device names are handled with proper case sensitivity and stripping"""
        # Test with extra whitespace
        result = get_interface_from_yaml(' R1 ', ' R2 ', 0, self.testbed_topology)
        self.assertEqual(result, 'GigabitEthernet0/0/0')

    def test_get_interface_with_segments(self):
        """Test getting interface when remote is a segment name"""
        # Test segment1
        result = get_interface_from_yaml('R1', 'segment1', 'segment1', self.testbed_topology_with_segments)
        self.assertEqual(result, 'GigabitEthernet0/0/0')

        # Test segment2
        result = get_interface_from_yaml('R1', 'segment2', 'segment2', self.testbed_topology_with_segments)
        self.assertEqual(result, 'GigabitEthernet0/0/1')

    def test_get_interface_with_segments_different_value(self):
        """Test segment functionality requires value to match segment in topology"""
        # The value parameter must match the segment name in the topology structure
        # This test demonstrates that when value != segment name, it returns empty list
        result = get_interface_from_yaml('R1', 'segment1', 'different_value', self.testbed_topology_with_segments)
        self.assertEqual(result, [])  # Returns empty list when value doesn't match segment structure

        # When value matches segment name, it works properly
        result = get_interface_from_yaml('R1', 'segment1', 'segment1', self.testbed_topology_with_segments)
        self.assertEqual(result, 'GigabitEthernet0/0/0')

    def test_get_interface_with_nonexistent_segment(self):
        """Test behavior when remote segment doesn't exist in local segments"""
        # When segment doesn't exist, it falls back to device alias resolution which fails
        with self.assertRaises(Exception) as context:
            get_interface_from_yaml('R1', 'nonexistent_segment', 0, self.testbed_topology_with_segments)

        # The actual error depends on the fallback behavior - could be list index out of range
        # from device alias resolution or link processing
        self.assertTrue(
            "list index out of range" in str(context.exception) or
            "does not exists" in str(context.exception)
        )

    def test_get_interface_segments_priority_over_links(self):
        """Test that segment matching takes priority over link matching"""
        # Create topology where device has both segments and links
        mixed_topology = {
            'R1': {
                'interfaces': {
                    'GigabitEthernet0/0/0': {
                        'segment': 'test_segment',
                        'link': 'R1_R2_1',
                        'type': 'ethernet'
                    },
                    'GigabitEthernet0/0/1': {
                        'link': 'R1_R2_1',
                        'type': 'ethernet'
                    }
                }
            },
            'R2': {
                'interfaces': {
                    'GigabitEthernet0/0/0': {
                        'link': 'R1_R2_1',
                        'type': 'ethernet'
                    }
                }
            }
        }

        # When remote is a segment name, segment logic should be used
        result = get_interface_from_yaml('R1', 'test_segment', 'test_segment', mixed_topology)
        self.assertEqual(result, 'GigabitEthernet0/0/0')


class TestManagementGatewayInference(unittest.TestCase):
    """Coverage for the management gateway detection/inference helpers.

    These exercise the decision logic directly (rather than fully mocking
    ``get_mgmt_ip_and_mgmt_src_ip_addresses``) and include the negative cases
    that must NOT be classified as gateway/NAT traffic.
    """

    # ---- _infer_management_gateway_addresses -----------------------------

    def test_infer_requires_explicit_prefix(self):
        # A bare address (no prefix) must never manufacture a /24 subnet.
        self.assertEqual(
            _infer_management_gateway_addresses(
                '192.168.122.77', ['192.168.122.1']),
            set())

    def test_infer_with_24_prefix_matches_first_usable(self):
        self.assertEqual(
            _infer_management_gateway_addresses(
                '192.168.122.77/24', ['192.168.122.1']),
            {'192.168.122.1'})

    def test_infer_with_24_prefix_matches_last_usable(self):
        self.assertEqual(
            _infer_management_gateway_addresses(
                '192.168.122.77/24', ['192.168.122.254']),
            {'192.168.122.254'})

    def test_infer_non_24_prefix_16_does_not_flag_dot254(self):
        # On a /16 the last usable address is 10.0.255.254, so a legitimate
        # 10.0.0.254 peer must NOT be treated as a gateway (the old /24
        # assumption would have wrongly flagged it).
        self.assertEqual(
            _infer_management_gateway_addresses(
                '10.0.0.5/16', ['10.0.0.254']),
            set())

    def test_infer_non_24_prefix_16_matches_real_gateways(self):
        # /16 gateways are 10.0.0.1 (first usable) and 10.0.255.254 (last usable)
        self.assertEqual(
            _infer_management_gateway_addresses(
                '10.0.0.5/16', ['10.0.0.1', '10.0.255.254', '10.0.0.254']),
            {'10.0.0.1', '10.0.255.254'})

    def test_infer_non_24_prefix_25_does_not_flag_other_subnet_dot1(self):
        # mgmt 10.0.0.130/25 lives in subnet 10.0.0.128/25, so a legitimate
        # 10.0.0.1 peer (a different subnet) must NOT be flagged.
        self.assertEqual(
            _infer_management_gateway_addresses(
                '10.0.0.130/25', ['10.0.0.1']),
            set())

    def test_infer_non_24_prefix_25_matches_subnet_gateways(self):
        # subnet 10.0.0.128/25 -> first usable .129, last usable .254
        self.assertEqual(
            _infer_management_gateway_addresses(
                '10.0.0.130/25', ['10.0.0.129', '10.0.0.254']),
            {'10.0.0.129', '10.0.0.254'})

    # ---- _management_session_uses_gateway --------------------------------

    def _device(self, management):
        device = MagicMock()
        device.management = management
        return device

    def test_configured_gateway_match_returns_true(self):
        device = self._device({'gateway': {'ipv4': '192.168.122.1'}})
        self.assertTrue(
            _management_session_uses_gateway(
                device, ['192.168.122.1'], mgmt_ip='192.168.122.77'))

    def test_configured_gateway_mismatch_returns_false(self):
        # Authoritative topology data: configured gateway .254 but session peer
        # .1 -> must return False rather than fall back to inference.
        device = self._device({
            'gateway': {'ipv4': '192.168.122.254'},
            'address': {'ipv4': IPv4Interface('192.168.122.77/24')},
        })
        self.assertFalse(
            _management_session_uses_gateway(
                device, ['192.168.122.1'], mgmt_ip='192.168.122.77'))

    def test_inference_uses_configured_address_prefix(self):
        # No configured gateway; prefix comes from device.management address.
        device = self._device({
            'address': {'ipv4': IPv4Interface('10.0.0.5/16')}})
        self.assertTrue(
            _management_session_uses_gateway(
                device, ['10.0.0.1'], mgmt_ip='10.0.0.5'))

    def test_legit_dot254_peer_not_classified_as_nat_on_16(self):
        # No configured gateway, /16 prefix; a legitimate 10.0.0.254 peer must
        # NOT be classified as gateway/NAT.
        device = self._device({
            'address': {'ipv4': IPv4Interface('10.0.0.5/16')}})
        self.assertFalse(
            _management_session_uses_gateway(
                device, ['10.0.0.254'], mgmt_ip='10.0.0.5'))

    def test_no_prefix_available_skips_inference(self):
        # address is 'dhcp' (a plain string with no prefix) -> no inference.
        device = self._device({'address': {'ipv4': 'dhcp'}})
        self.assertFalse(
            _management_session_uses_gateway(
                device, ['192.168.122.1'], mgmt_ip='192.168.122.77'))

    def test_multiple_addresses_selects_interface_matching_mgmt_ip(self):
        # ``address.ipv4`` may be a list of interfaces. The one whose .ip
        # matches mgmt_ip must be selected so inference uses the right subnet.
        device = self._device({'address': {'ipv4': [
            IPv4Interface('192.168.50.5/24'),
            IPv4Interface('10.0.0.5/16'),
        ]}})
        # mgmt_ip matches the /16 interface -> 10.0.0.1 is inferred as gateway.
        self.assertTrue(
            _management_session_uses_gateway(
                device, ['10.0.0.1'], mgmt_ip='10.0.0.5'))

    def test_multiple_addresses_uses_matching_subnet_not_others(self):
        # With a list of addresses, a peer that would only be a gateway in a
        # non-selected subnet must NOT be flagged. Here mgmt_ip matches the
        # /16 interface (gateways 10.0.0.1 / 10.0.255.254); 192.168.50.1 is the
        # gateway of the OTHER configured subnet and must not match.
        device = self._device({'address': {'ipv4': [
            IPv4Interface('192.168.50.5/24'),
            IPv4Interface('10.0.0.5/16'),
        ]}})
        self.assertFalse(
            _management_session_uses_gateway(
                device, ['192.168.50.1'], mgmt_ip='10.0.0.5'))

    def test_multiple_addresses_no_match_skips_inference(self):
        # When no configured interface matches mgmt_ip, skip inference rather
        # than borrowing an unrelated prefix (which could flag an unrelated peer
        # as the gateway and advertise an unreachable local address).
        device = self._device({'address': {'ipv4': [
            'dhcp',
            IPv4Interface('10.0.0.5/16'),
        ]}})
        self.assertFalse(
            _management_session_uses_gateway(
                device, ['10.0.0.1'], mgmt_ip='172.16.9.9'))


class TestManagementGatewayIosxrDataPath(unittest.TestCase):
    """Exercise the real IOS XR (spitfire/VXR) mgmt data path end-to-end.

    Instead of mocking ``get_mgmt_ip_and_mgmt_src_ip_addresses``, this parses
    real ``netstat`` output through the spitfire API and feeds the resulting
    (mgmt_ip, mgmt_src_ip_addresses) into the gateway classifier.
    """

    NETSTAT_OUTPUT = dedent('''
        Active Internet connections (servers and established)
        Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
        tcp        0      0 0.0.0.0:179             0.0.0.0:*               LISTEN      1131/bgp
        tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      7756/sshd
        tcp        0    188 1.1.1.95:22             2.2.2.145:50173         ESTABLISHED 12021/sshd: admin [
        tcp6       0      0 :::179                  :::*                    LISTEN      1131/bgp
    ''')

    def _xr_device(self, management):
        from genie.conf.base.device import Device as GenieDevice
        device = GenieDevice(
            name='Router',
            os='iosxr',
            platform='spitfire',
            custom=dict(abstraction=dict(order=['os', 'platform'])))
        device.is_connected = Mock(return_value=True)
        device.execute = Mock(return_value=self.NETSTAT_OUTPUT)
        device.management = management
        return device

    def _mgmt_data(self, device):
        from genie.libs.sdk.apis.iosxr.spitfire.utils import (
            get_mgmt_ip_and_mgmt_src_ip_addresses)
        return get_mgmt_ip_and_mgmt_src_ip_addresses(device)

    def test_xr_configured_gateway_match(self):
        device = self._xr_device({'gateway': {'ipv4': '2.2.2.145'}})
        mgmt_ip, mgmt_src_ip_addresses = self._mgmt_data(device)
        self.assertEqual(mgmt_ip, '1.1.1.95')
        self.assertEqual(set(mgmt_src_ip_addresses), {'2.2.2.145'})
        self.assertTrue(
            _management_session_uses_gateway(
                device, mgmt_src_ip_addresses, mgmt_ip=mgmt_ip))

    def test_xr_configured_gateway_mismatch(self):
        # Configured gateway does not match the observed session peer -> the
        # authoritative data must win and inference must not override it.
        device = self._xr_device({
            'gateway': {'ipv4': '2.2.2.254'},
            'address': {'ipv4': IPv4Interface('1.1.1.95/24')},
        })
        mgmt_ip, mgmt_src_ip_addresses = self._mgmt_data(device)
        self.assertFalse(
            _management_session_uses_gateway(
                device, mgmt_src_ip_addresses, mgmt_ip=mgmt_ip))

    def test_xr_dhcp_address_skips_inference(self):
        # A VXR sim device with 'dhcp' address and no matching gateway must not
        # be classified as gateway/NAT via inference.
        device = self._xr_device({
            'address': {'ipv4': 'dhcp'},
            'gateway': {'ipv4': '192.168.122.1'},
        })
        mgmt_ip, mgmt_src_ip_addresses = self._mgmt_data(device)
        # Session peer 2.2.2.145 does not match configured gateway, and the
        # 'dhcp' address provides no prefix -> no inference -> False.
        self.assertFalse(
            _management_session_uses_gateway(
                device, mgmt_src_ip_addresses, mgmt_ip=mgmt_ip))
