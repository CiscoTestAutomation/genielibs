
import re
import unittest
from unittest.mock import MagicMock, Mock, call, patch, PropertyMock


from ats.topology import Device
from unittest import mock

from genie.libs.clean.stages.tests.utils import create_test_device
from genie.libs.sdk.apis.utils import (
    modify_filename, copy_from_device, copy_to_device, device_recovery_boot,
    configure_management_console, configure_peripheral_terminal_server,
    time_to_int, slugify_filename, get_file_size_from_server,
    get_interface_from_yaml)


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
