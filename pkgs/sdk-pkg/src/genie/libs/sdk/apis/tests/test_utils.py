
import re
import socket
import unittest
from ipaddress import IPv4Interface
from textwrap import dedent
from types import SimpleNamespace
from unittest.mock import ANY, MagicMock, Mock, call, patch, PropertyMock


from ats.topology import Device
from pyats.topology.credentials import Credentials
from unittest import mock
from unicon.core.errors import SubCommandFailure

from genie.libs.clean.stages.tests.utils import create_test_device
from genie.libs.sdk.apis.utils import (
    modify_filename, copy_from_device, copy_to_device, device_recovery_boot,
    configure_management_console, configure_peripheral_terminal_server,
    time_to_int, slugify_filename, get_file_size_from_server,
    get_interface_from_yaml, convert_server_to_linux_device, get_proxy,
    _management_session_uses_gateway, _infer_management_gateway_addresses)
from genie.libs.sdk.apis.utils import (
    _probe_tcp_host, probe_tcp_host, probe_tcp_hosts, probe_tcp_from_server)


class TestUtilsApi(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'

    @patch('genie.libs.sdk.apis.utils.socket.create_connection')
    def test_probe_tcp_host_reachable(self, create_connection):
        result = probe_tcp_host(self.device, '192.0.2.1', 443)
        self.assertEqual(result, {
            'host': '192.0.2.1',
            'port': 443,
            'status': 'reachable',
            'reachable': True,
            'method': 'python',
            'output': None,
            'error': None,
        })
        create_connection.assert_called_once_with(('192.0.2.1', 443),
                                                   timeout=3)

    def test_probe_tcp_host_invalid_target(self):
        result = probe_tcp_host(self.device, '', 443)
        self.assertEqual(result, {
            'host': '',
            'port': 443,
            'status': 'invalid_target',
            'reachable': False,
            'method': None,
            'output': None,
            'error': 'host must be a valid IP address or hostname',
        })

    @patch('genie.libs.sdk.apis.utils.socket.create_connection')
    def test_probe_tcp_host_timeout(self, create_connection):
        create_connection.side_effect = socket.timeout('timed out')

        result = probe_tcp_host(self.device, 'example.com', 443, timeout=1)

        self.assertEqual(result, {
            'host': 'example.com',
            'port': 443,
            'status': 'timeout',
            'reachable': False,
            'method': 'python',
            'output': None,
            'error': 'timed out',
        })

    @patch('genie.libs.sdk.apis.utils.socket.create_connection')
    def test_probe_tcp_host_unreachable(self, create_connection):
        create_connection.side_effect = ConnectionRefusedError('refused')

        result = _probe_tcp_host('example.com', 22)

        self.assertEqual(result, {
            'host': 'example.com',
            'port': 22,
            'status': 'unreachable',
            'reachable': False,
            'method': 'python',
            'output': None,
            'error': 'refused',
        })

    @patch('genie.libs.sdk.apis.utils._probe_tcp_host')
    def test_probe_tcp_hosts_preserves_input_order(self, probe):
        probe.side_effect = lambda host, port, timeout: {
            'host': host, 'port': port, 'status': 'reachable',
            'reachable': True, 'method': 'python', 'output': None,
            'error': None}
        result = probe_tcp_hosts(self.device, ['one', 'two'], 22, workers=2)
        self.assertEqual([item['host'] for item in result], ['one', 'two'])
        self.assertEqual(probe.call_count, 2)

    def test_probe_tcp_from_server_prefers_nmap(self):
        remote = MagicMock()
        stdout = 'Host: 192.0.2.1 ()\tPorts: 443/open/tcp//https///'
        remote.execute.side_effect = [
            '/usr/bin/nmap', '{}\n__GENIE_NMAP_RC__=0\n'.format(stdout)]
        result = probe_tcp_from_server(self.device, remote, '192.0.2.1', 443)
        self.assertEqual(result, [{
            'host': '192.0.2.1',
            'port': 443,
            'reachable': True,
            'status': 'reachable',
            'method': 'remote',
            'tool': 'nmap',
            'command': remote.execute.call_args_list[1][0][0],
            'stdout': stdout,
            'stderr': '',
            'error': None,
            'elapsed': ANY,
            'output': stdout,
        }])
        self.assertIn('nmap -Pn', remote.execute.call_args_list[1][0][0])

    def test_probe_tcp_accepts_unconnected_server_device(self):
        class Remote:
            def connect(remote_self):
                remote_self.execute = Mock(side_effect=[
                    '/usr/bin/nmap',
                    ('Host: 192.0.2.1 ()\tPorts: '
                     '443/open/tcp//https///\n__GENIE_NMAP_RC__=0\n'),
                ])

        remote = Remote()
        with patch(
                'genie.libs.sdk.apis.utils.convert_server_to_linux_device'
        ) as converter:
            result = probe_tcp_from_server(
                self.device, remote, '192.0.2.1', 443)

        converter.assert_not_called()
        self.assertTrue(result[0]['reachable'])

    def test_probe_tcp_from_server_uses_exact_ipv6_nmap_command(self):
        remote = MagicMock()
        remote.execute.side_effect = [
            '/usr/bin/nmap',
            ('Host: 2001:db8::1 ()\tPorts: 22/open/tcp//ssh///\n'
             '__GENIE_NMAP_RC__=0\n')]

        probe_tcp_from_server(self.device, remote, '2001:db8::1', 22)

        remote.execute.assert_has_calls([
            call('command -v nmap'),
            call("nmap -6 -Pn -n -p 22 --host-timeout 3s -oG - "
                 "2001:db8::1 2>&1; status=$?; printf "
                 "'\\n__GENIE_NMAP_RC__=%s\\n' \"$status\"",
                 timeout=8.0),
        ])

    def test_probe_tcp_from_server_uses_nc_exit_status_marker(self):
        remote = MagicMock()
        remote.execute.side_effect = [
            '', '/usr/bin/nc',
            '__GENIE_NC_RC__=0\nConnection to 2001:db8::1 succeeded']
        result = probe_tcp_from_server(
            self.device, remote, '2001:db8::1', 22, timeout=3.0)
        self.assertTrue(result[0]['reachable'])
        self.assertEqual(result[0]['tool'], 'nc')
        self.assertEqual(
            result[0]['stderr'], 'Connection to 2001:db8::1 succeeded')
        command = remote.execute.call_args_list[2][0][0]
        self.assertIn('nc -6 -vz', command)
        self.assertIn('-w 3 ', command)
        self.assertNotIn('-w 3.0 ', command)
        self.assertIn('__GENIE_NC_RC__', command)

    def test_probe_tcp_from_server_accepts_ncat_crlf_output(self):
        remote = MagicMock()
        remote.execute.side_effect = [
            '', '/usr/bin/nc',
            ('__GENIE_NC_RC__=0\r\n'
             'Ncat: Version 7.92 ( https://nmap.org/ncat )\r\n'
             'Ncat: Connected to 5.28.18.8:22.\r\n'),
        ]

        result = probe_tcp_from_server(
            self.device, remote, '5.28.18.8', 22, timeout=5)

        self.assertTrue(result[0]['reachable'])
        self.assertEqual(result[0]['status'], 'reachable')
        self.assertIn('Ncat: Connected', result[0]['stderr'])

    def test_probe_tcp_from_server_falls_back_when_nmap_cannot_execute(self):
        remote = MagicMock()
        remote.execute.side_effect = [
            '/usr/bin/nmap',
            'nmap: command not found\n__GENIE_NMAP_RC__=127\n',
            '/usr/bin/nc', '__GENIE_NC_RC__=0\nConnection succeeded']
        result = probe_tcp_from_server(self.device, remote, '192.0.2.1', 443)
        self.assertTrue(result[0]['reachable'])
        self.assertEqual(result[0]['tool'], 'nc')
        self.assertEqual(remote.execute.call_args_list[2], call('command -v nc'))
        self.assertIn('nc -vz', remote.execute.call_args_list[3][0][0])

    def test_probe_tcp_from_server_does_not_fallback_after_valid_result(self):
        cases = (
            (('Host: 192.0.2.1 ()\tPorts: 443/closed/tcp//https///\n'
              '__GENIE_NMAP_RC__=0\n'), 'unreachable'),
            ('Host timed out\n__GENIE_NMAP_RC__=0\n', 'timeout'),
        )
        for output, status in cases:
            with self.subTest(status=status):
                remote = MagicMock()
                remote.execute.side_effect = ['/usr/bin/nmap', output]

                result = probe_tcp_from_server(
                    self.device, remote, '192.0.2.1', 443)

                self.assertEqual(result[0]['status'], status)
                self.assertEqual(result[0]['method'], 'remote')
                self.assertEqual(remote.execute.call_count, 2)

    def test_probe_tcp_from_server_rejects_misleading_nmap_diagnostic(self):
        remote = MagicMock()
        remote.execute.side_effect = [
            '/usr/bin/nmap',
            'Failed to open device eth0\n__GENIE_NMAP_RC__=1\n']

        result = probe_tcp_from_server(
            self.device, remote, '192.0.2.1', 443)

        self.assertFalse(result[0]['reachable'])
        self.assertEqual(result[0]['status'], 'execution_error')
        self.assertEqual(result[0]['tool'], 'nmap')
        self.assertEqual(remote.execute.call_count, 2)

    def test_probe_tcp_requires_target_host_record(self):
        remote = MagicMock()
        remote.execute.side_effect = [
            '/usr/bin/nmap',
            ('WARNING: Ports: 443/open/tcp//https///\n'
             'Host: 198.51.100.2 ()\tPorts: 443/open/tcp//https///\n'
             '__GENIE_NMAP_RC__=0\n')]

        result = probe_tcp_from_server(
            self.device, remote, '192.0.2.1', 443)

        self.assertFalse(result[0]['reachable'])
        self.assertEqual(result[0]['status'], 'unreachable')
        self.assertEqual(result[0]['method'], 'remote')
        self.assertEqual(result[0]['tool'], 'nmap')

    def test_probe_tcp_capability_exceptions_do_not_fallback(self):
        cases = (
            (socket.timeout('capability timed out'), 'timeout'),
            (OSError('transport failed'), 'transport_error'),
            (SubCommandFailure('capability command failed'),
             'execution_error'),
        )
        for error, status in cases:
            with self.subTest(status=status):
                remote = MagicMock()
                remote.execute.side_effect = error

                result = probe_tcp_from_server(
                    self.device, remote, '192.0.2.1', 443)

                self.assertEqual(result[0]['status'], status)
                self.assertEqual(result[0]['tool'], 'nmap')
                self.assertEqual(result[0]['command'], 'command -v nmap')
                self.assertEqual(result[0]['error'], str(error))
                self.assertEqual(remote.execute.call_count, 1)

    def test_probe_tcp_from_server_reports_unavailable(self):
        remote = MagicMock()
        remote.execute.side_effect = ['', '']

        result = probe_tcp_from_server(
            self.device, remote, 'example.com', 443)

        self.assertEqual(result, [{
            'host': 'example.com',
            'port': 443,
            'reachable': False,
            'status': 'unavailable',
            'method': 'remote',
            'tool': None,
            'command': None,
            'stdout': '',
            'stderr': '',
            'error': 'nmap and nc are not available',
            'elapsed': 0.0,
            'output': None,
        }])

    def test_probe_tcp_from_server_rejects_option_injection(self):
        remote = MagicMock()

        result = probe_tcp_from_server(
            self.device, remote, '--script=default', 443)

        self.assertEqual(result, [{
            'host': '--script=default',
            'port': 443,
            'reachable': False,
            'status': 'invalid_target',
            'method': 'remote',
            'tool': None,
            'command': None,
            'stdout': '',
            'stderr': '',
            'error': 'host must not begin with "-"',
            'elapsed': 0.0,
            'output': None,
        }])
        remote.execute.assert_not_called()

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

    @patch('genie.libs.sdk.apis.utils.FileUtils.from_device')
    def test_copy_from_device_supports_server_port(self, from_device):
        device = MagicMock()
        file_utils = from_device.return_value
        file_utils.get_server_block.return_value = {'protocol': 'https'}
        file_utils.get_hostname.return_value = 'server.example.com'

        copy_from_device(device, local_path='flash:test.txt',
                         remote_path='uploads/test.txt', server='server',
                         protocol='https', port=8443)

        file_utils.copyfile.assert_called_once_with(
            source='flash:test.txt',
            destination='https://server.example.com:8443/uploads/test.txt',
            device=device,
            timeout_seconds=300)

    @patch('genie.libs.sdk.apis.utils.FileUtils.from_device')
    def test_copy_from_device_supports_server_port_and_vrf(self, from_device):
        device = MagicMock()
        file_utils = from_device.return_value
        file_utils.get_server_block.return_value = {'protocol': 'https'}
        file_utils.get_hostname.return_value = 'management.example.com'

        copy_from_device(device, local_path='flash:test.txt',
                         remote_path='uploads/test.txt', server='server',
                         protocol='https', vrf='management', port=8443)

        file_utils.get_hostname.assert_called_once_with(
            'server', device, vrf='management')
        file_utils.copyfile.assert_called_once_with(
            source='flash:test.txt',
            destination=(
                'https://management.example.com:8443/uploads/test.txt'),
            device=device,
            vrf='management',
            timeout_seconds=300)

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

    @patch('genie.libs.sdk.apis.utils.FileUtils')
    @patch('genie.libs.sdk.apis.utils.FileServer')
    @patch(
        'genie.libs.sdk.apis.proxy_selection.select_runtime_proxy_for_device')
    @patch(
        'genie.libs.sdk.apis.proxy_selection.proxy_selection_config',
        return_value={'mode': 'runtime'})
    def test_copy_from_device_uses_connected_runtime_proxy(
            self, _config, selector, file_server, file_utils):
        device = MagicMock()
        device.hostname = 'router'
        device.os = 'iosxe'
        device.management = {
            'address': {'ipv4': IPv4Interface('127.0.0.2/24')},
            'interface': 'Management0',
        }
        device.api.get_proxy.return_value = 'legacy-proxy'
        proxy = MagicMock()
        proxy.api.get_local_ip.return_value = '127.0.0.1'
        proxy.api.get_route_iface_source_ip.return_value = (
            'eth0', '127.0.0.2')
        proxy.api.socat_relay.return_value = 2000
        selector.return_value = {
            'server_name': 'route-proxy', 'proxy_device': proxy,
            'device_ip': '127.0.0.2', 'connected': True,
        }
        server_context = file_server.return_value.__enter__.return_value
        server_context.get.side_effect = lambda key, default=None: {
            'port': 8080,
            'credentials': {'http': {'username': 'user', 'password': 'pass'}},
        }.get(key, default)
        fu = file_utils.from_device.return_value

        copy_from_device(
            device, local_path='flash:test.txt', protocol='http')

        selector.assert_called_once_with(
            device, fallback_proxy='legacy-proxy',
            server_converter=device.api.convert_server_to_linux_device,
            target_prober=device.api.probe_tcp_from_server)
        proxy.connect.assert_not_called()
        self.assertEqual(
            fu.copyfile.call_args.kwargs['destination'],
            'http://user:pass@127.0.0.2:2000/router_test.txt')

    @patch('genie.libs.sdk.apis.utils.FileUtils')
    @patch('genie.libs.sdk.apis.utils.FileServer')
    def test_copy_flow_keeps_current_fallback_over_unrouted_global_candidate(
            self, file_server, file_utils):
        class Proxy:
            def __init__(self):
                self.connected = False
                self.connect = Mock(side_effect=self._connect)
                self.api = SimpleNamespace(
                    get_local_ip=Mock(return_value='127.0.0.1'),
                    get_route_iface_source_ip=Mock(
                        return_value=('eth0', '127.0.0.2')),
                    socat_relay=Mock(return_value=2000))

            def _connect(self):
                self.connected = True

            def is_connected(self):
                return self.connected

        global_proxy, current_proxy = Proxy(), Proxy()
        services = {'ssh': {
            'application': 'proxy', 'protocol': 'ssh', 'port': 2201,
            'order': 1}}
        servers = {
            'global': {
                'services': services,
                'management': {'routes': {'ipv4': [{
                    'subnet': '192.0.2.0/24', 'interface': 'eth0'}]}},
                'interfaces': {'eth0': {'ipv4': '192.0.2.10/24'}},
            },
            'current': {'services': services},
        }
        proxies = {'global': global_proxy, 'current': current_proxy}
        api = SimpleNamespace(
            get_proxy=Mock(return_value='current'),
            convert_server_to_linux_device=Mock(
                side_effect=lambda name: proxies[name]),
            probe_tcp_from_server=Mock())
        device = SimpleNamespace(
            name='router', hostname='router', os='iosxe', via='cli',
            connections={'cli': {'port': 22}}, custom={}, api=api,
            management={
                'address': {'ipv4': IPv4Interface('10.20.1.5/24')},
                'interface': 'Management0'},
            testbed=SimpleNamespace(
                custom={'proxy_selection': {
                    'mode': 'runtime', 'candidates': ['global']}},
                servers=servers, devices=proxies))
        fs = file_server.return_value.__enter__.return_value
        fs.get.side_effect = lambda key, default=None: {
            'port': 8080,
            'credentials': {'http': {
                'username': 'user', 'password': 'pass'}},
        }.get(key, default)

        copy_from_device(
            device, local_path='flash:test.txt', protocol='http')

        global_proxy.connect.assert_not_called()
        current_proxy.connect.assert_called_once_with()
        destination = file_utils.from_device.return_value.copyfile.call_args \
            .kwargs['destination']
        self.assertEqual(
            destination, 'http://user:pass@127.0.0.2:2000/router_test.txt')

    def test_copy_flows_retry_next_runtime_candidate_after_relay_failure(self):
        class Proxy:
            def __init__(self, relay):
                self.connected = False
                self.connect = Mock(side_effect=self._connect)
                self.api = SimpleNamespace(
                    get_local_ip=Mock(return_value='127.0.0.1'),
                    get_route_iface_source_ip=Mock(
                        return_value=('eth0', '127.0.0.2')),
                    socat_relay=relay)

            def _connect(self):
                self.connected = True

            def is_connected(self):
                return self.connected

        server = {
            'management': {'routes': {'ipv4': [{
                'subnet': '10.20.0.0/16', 'interface': 'eth0'}]}},
            'interfaces': {'eth0': {'ipv4': '192.0.2.10/24'}},
        }
        file_utils_path = 'genie.libs.sdk.apis.utils.FileUtils'
        file_server_path = 'genie.libs.sdk.apis.utils.FileServer'
        for relay_failure in ('exception', 'empty'):
            for direction in ('to', 'from'):
                with self.subTest(
                        relay_failure=relay_failure, direction=direction), \
                        patch(file_utils_path) as file_utils, \
                        patch(file_server_path) as file_server:
                    first_relay = (Mock(
                        side_effect=RuntimeError('relay failed'))
                        if relay_failure == 'exception'
                        else Mock(return_value=None))
                    first = Proxy(first_relay)
                    second = Proxy(Mock(return_value=2000))
                    proxies = {'first': first, 'second': second}
                    api = SimpleNamespace(
                        get_proxy=Mock(return_value=None),
                        convert_server_to_linux_device=Mock(
                            side_effect=lambda name: proxies[name]),
                        probe_tcp_from_server=Mock())
                    device = SimpleNamespace(
                        name='router', hostname='router', os='iosxe',
                        via='cli', connections={'cli': {'port': 22}},
                        custom={'proxy_selection': {
                            'candidates': ['first', 'second']}}, api=api,
                        management={
                            'address': {
                                'ipv4': IPv4Interface('10.20.1.5/24')},
                            'interface': 'Management0'},
                        testbed=SimpleNamespace(
                            custom={'proxy_selection': {'mode': 'runtime'}},
                            servers={'first': server, 'second': server},
                            devices=proxies))
                    fs = file_server.return_value.__enter__.return_value
                    fs.get.side_effect = lambda key, default=None: {
                        'port': 8080,
                        'credentials': {'http': {
                            'username': 'user', 'password': 'pass'}},
                    }.get(key, default)

                    if direction == 'to':
                        copy_to_device(
                            device, remote_path='/tmp/test.txt',
                            protocol='http')
                    else:
                        copy_from_device(
                            device, local_path='flash:test.txt',
                            protocol='http')

                    first.api.socat_relay.assert_called_once_with(
                        remote_ip='127.0.0.1', remote_port=8080,
                        protocol='TCP4')
                    second.api.socat_relay.assert_called_once_with(
                        remote_ip='127.0.0.1', remote_port=8080,
                        protocol='TCP4')
                    copyfile = file_utils.from_device.return_value.copyfile
                    self.assertEqual(copyfile.call_count, 1)

    @patch('genie.libs.sdk.apis.utils.FileUtils')
    @patch('genie.libs.sdk.apis.utils.FileServer')
    @patch(
        'genie.libs.sdk.apis.proxy_selection.select_runtime_proxy_for_device')
    @patch(
        'genie.libs.sdk.apis.proxy_selection.invalidate_runtime_proxy_cache')
    def test_copyfile_error_does_not_invalidate_or_reselect_proxy(
            self, invalidate, selector, file_server, file_utils):
        proxy = MagicMock()
        proxy.api.get_local_ip.return_value = '127.0.0.1'
        proxy.api.get_route_iface_source_ip.return_value = (
            'eth0', '127.0.0.2')
        proxy.api.socat_relay.return_value = 2000
        selector.return_value = {
            'server_name': 'proxy-a', 'proxy_device': proxy,
            'device_ip': '10.20.1.5', 'connected': True,
        }
        api = SimpleNamespace(
            get_proxy=Mock(return_value='proxy-a'),
            convert_server_to_linux_device=Mock(return_value=proxy),
            probe_tcp_from_server=Mock())
        device = SimpleNamespace(
            name='router', hostname='router', os='iosxe', via='cli',
            connections={'cli': {'port': 22}}, custom={}, api=api,
            management={
                'address': {'ipv4': IPv4Interface('10.20.1.5/24')},
                'interface': 'Management0'},
            testbed=SimpleNamespace(
                custom={'proxy_selection': {'mode': 'runtime'}},
                servers={'proxy-a': {}}, devices={}))
        fs = file_server.return_value.__enter__.return_value
        fs.get.side_effect = lambda key, default=None: {
            'port': 8080,
            'credentials': {'http': {
                'username': 'user', 'password': 'pass'}},
        }.get(key, default)
        fu = file_utils.from_device.return_value
        errors = (
            FileNotFoundError('source file missing'),
            OSError('destination filesystem full'),
            SubCommandFailure('device rejected copy'),
        )
        for error in errors:
            with self.subTest(error=type(error).__name__):
                selector.reset_mock()
                invalidate.reset_mock()
                proxy.api.socat_relay.reset_mock()
                fu.copyfile.reset_mock()
                fu.copyfile.side_effect = error

                result = copy_from_device(
                    device, local_path='flash:test.txt', protocol='http')

                self.assertIsNone(result)
                selector.assert_called_once()
                invalidate.assert_not_called()
                proxy.api.socat_relay.assert_called_once()
                fu.copyfile.assert_called_once()

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

    def test_convert_server_preserves_ordered_ssh_services_and_port(self):
        device = MagicMock()
        services = {
            'ssh-maintenance': {
                'application': 'maintenance', 'protocol': 'ssh',
                'port': 2222, 'order': 0,
            },
            'ssh-later': {
                'application': 'proxy', 'protocol': 'ssh',
                'port': 2202, 'order': 2,
            },
            'ssh-first': {
                'application': 'proxy', 'protocol': 'ssh',
                'port': 2201, 'order': 1,
            },
            'file-transfer': {
                'application': 'files', 'protocol': 'scp',
                'port': 22, 'order': 0,
            },
        }
        server_block = {
            'address': '192.0.2.10',
            'credentials': {'default': {
                'username': 'user', 'password': 'pass'}},
            'services': services,
            'custom': {'rack': 'rack-a'},
        }
        device.testbed.servers = {'proxy': server_block}
        fileutils = MagicMock()
        fileutils.get_server_block.return_value = server_block
        fileutils.get_hostname.return_value = '192.0.2.10'

        with patch('genie.libs.sdk.apis.utils.FileUtils') as fileutils_cls, \
                patch('genie.libs.sdk.apis.utils.Device') as device_cls:
            fileutils_cls.return_value.__enter__.return_value = fileutils
            convert_server_to_linux_device(device, 'proxy')

        kwargs = device_cls.call_args.kwargs
        self.assertEqual(kwargs['connections']['linux']['port'], 2201)
        self.assertEqual(
            kwargs['connections']['linux']['ssh_options'],
            '-o PasswordAuthentication=yes')
        self.assertEqual(list(kwargs['services']), list(services))
        self.assertEqual(kwargs['services'], services)
        self.assertEqual(kwargs['server_metadata']['services'], services)
        self.assertEqual(kwargs['custom']['rack'], 'rack-a')

    def test_convert_server_does_not_deepcopy_credentials_as_metadata(self):
        device = MagicMock()
        credentials = Credentials({
            'default': {'username': 'user', 'password': 'pass'},
        })
        server_block = {
            'address': '192.0.2.10',
            'credentials': credentials,
            'services': {'ssh': {'protocol': 'ssh', 'port': 22}},
        }
        device.testbed.servers = {'proxy': server_block}
        fileutils = MagicMock()
        fileutils.get_server_block.return_value = server_block
        fileutils.get_hostname.return_value = '192.0.2.10'

        with patch('genie.libs.sdk.apis.utils.FileUtils') as fileutils_cls, \
                patch('genie.libs.sdk.apis.utils.Device') as device_cls:
            fileutils_cls.return_value.__enter__.return_value = fileutils
            convert_server_to_linux_device(device, 'proxy')

        kwargs = device_cls.call_args.kwargs
        self.assertIs(kwargs['credentials'], credentials)
        self.assertNotIn('credentials', kwargs['server_metadata'])

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

    @patch('genie.libs.sdk.apis.utils.FileUtils.from_device')
    def test_copy_to_device_preserves_positional_vrf_with_port(
            self, from_device):
        device = MagicMock()
        file_utils = from_device.return_value
        file_utils.get_server_block.return_value = {'protocol': 'https'}
        file_utils.get_hostname.return_value = '10.0.0.1'

        copy_to_device(
            device, 'image.bin', 'bootflash:image.bin', 'server', 'https',
            'management', port=8443)

        file_utils.get_hostname.assert_called_once_with(
            'server', device, vrf='management')
        file_utils.copyfile.assert_called_once_with(
            source='https://10.0.0.1:8443/image.bin',
            destination='bootflash:image.bin',
            device=device,
            vrf='management',
            timeout_seconds=300,
            compact=False,
            use_kstack=False,
            protocol='https')

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

    @patch(
        'genie.libs.sdk.apis.proxy_selection.select_runtime_proxy_for_device')
    @patch(
        'genie.libs.sdk.apis.proxy_selection.proxy_selection_config',
        return_value=None)
    def test_copy_to_device_default_does_not_select_runtime_proxy(
            self, _config, selector):
        device = MagicMock()
        device.os = 'iosxe'
        device.management = {
            'address': {'ipv4': IPv4Interface('127.0.0.2/24')}}
        proxy = MagicMock()
        proxy.api.get_local_ip.return_value = '127.0.0.1'
        proxy.api.get_route_iface_source_ip.return_value = (None, '127.0.0.2')
        proxy.api.socat_relay.return_value = 2000
        device.api.get_proxy.return_value = 'legacy-proxy'
        device.api.convert_server_to_linux_device.return_value = proxy
        device.execute = Mock()

        copy_to_device(device, remote_path='/tmp/test.txt', protocol='http')

        selector.assert_not_called()
        device.api.get_proxy.assert_called_once_with()
        proxy.connect.assert_called_once_with()

    @patch('genie.libs.sdk.apis.utils.FileUtils')
    @patch('genie.libs.sdk.apis.utils.FileServer')
    @patch(
        'genie.libs.sdk.apis.proxy_selection.select_runtime_proxy_for_device')
    @patch(
        'genie.libs.sdk.apis.proxy_selection.proxy_selection_config',
        return_value={'mode': 'runtime'})
    def test_copy_to_device_runtime_proxy_is_already_connected_and_ipv6_safe(
            self, _config, selector, file_server, file_utils):
        device = MagicMock()
        device.os = 'iosxe'
        device.management = {
            'address': {'ipv6': '2001:db8:2::10/64'},
            'interface': 'Management0',
        }
        device.api.get_proxy.return_value = 'legacy-proxy'
        proxy = MagicMock()
        proxy.api.get_local_ip.return_value = '2001:db8:1::100'
        proxy.api.get_route_iface_source_ip.return_value = (
            'eth0', '2001:db8:1::1')
        proxy.api.socat_relay.return_value = 2000
        selector.return_value = {
            'server_name': 'route-proxy', 'proxy_device': proxy,
            'device_ip': '2001:db8:2::10', 'connected': True,
        }
        server_context = file_server.return_value.__enter__.return_value
        server_context.get.side_effect = lambda key, default=None: {
            'port': 8080,
            'credentials': {'http': {'username': 'user', 'password': 'pass'}},
        }.get(key, default)
        fu = file_utils.from_device.return_value

        copy_to_device(device, remote_path='/tmp/test.txt', protocol='http')

        selector.assert_called_once_with(
            device, fallback_proxy='legacy-proxy',
            server_converter=device.api.convert_server_to_linux_device,
            target_prober=device.api.probe_tcp_from_server)
        proxy.connect.assert_not_called()
        proxy.api.socat_relay.assert_called_once_with(
            remote_ip='2001:db8:1::100', remote_port=8080, protocol='TCP6')
        self.assertEqual(
            fu.copyfile.call_args.kwargs['source'],
            'http://user:pass@[2001:db8:1::1]:2000/test.txt')

    @patch('genie.libs.sdk.apis.utils.FileUtils')
    @patch('genie.libs.sdk.apis.utils.FileServer')
    def test_copy_to_device_uses_real_runtime_route_and_probe_helpers(
            self, file_server, file_utils):
        class Proxy:
            def __init__(self):
                self.connected = False
                self.connect = Mock(side_effect=self._connect)
                self.execute = Mock(side_effect=[
                    '/usr/bin/nmap',
                    ('Host: 10.20.1.5 ()\tPorts: '
                     '2022/open/tcp//ssh///\n__GENIE_NMAP_RC__=0\n'),
                ])
                self.api = SimpleNamespace(
                    get_local_ip=Mock(return_value='192.0.2.10'),
                    get_route_iface_source_ip=Mock(
                        return_value=('eth0', '192.0.2.1')),
                    socat_relay=Mock(return_value=2000),
                )

            def _connect(self):
                self.connected = True

            def is_connected(self):
                return self.connected

        proxy = Proxy()
        server = {
            'services': {'ssh': {
                'application': 'proxy', 'protocol': 'ssh', 'port': 2201}},
            'management': {'routes': {'ipv4': [{
                'subnet': '10.20.0.0/16', 'interface': 'eth0'}]}},
            'interfaces': {'eth0': {'ipv4': '192.0.2.10/24'}},
        }
        api = SimpleNamespace(
            get_proxy=Mock(return_value=None),
            convert_server_to_linux_device=Mock(return_value=proxy),
        )
        device = SimpleNamespace(
            name='router', hostname='router', os='iosxe', via='cli',
            connections={'cli': {'protocol': 'ssh', 'port': 2022}},
            custom={}, api=api,
            management={
                'address': {'ipv4': IPv4Interface('10.20.1.5/24')},
                'interface': 'Management0'},
            testbed=SimpleNamespace(
                custom={'proxy_selection': {
                    'mode': 'runtime', 'candidates': ['proxy'],
                    'target_probe': True}},
                servers={'proxy': server}, devices={'proxy': proxy}),
        )
        api.probe_tcp_from_server = lambda remote, hosts, port, timeout: \
            probe_tcp_from_server(
                device, remote, hosts, port, timeout=timeout)
        fs = file_server.return_value.__enter__.return_value
        fs.get.side_effect = lambda key, default=None: {
            'port': 8080,
            'credentials': {'http': {
                'username': 'user', 'password': 'pass'}},
        }.get(key, default)

        copy_to_device(device, remote_path='/tmp/test.txt', protocol='http')

        result = next(iter(device._runtime_proxy_cache['selected'].values()))
        self.assertEqual(result['server_name'], 'proxy')
        self.assertEqual(result['device_ip'], '10.20.1.5')
        self.assertEqual(result['target_port'], 2022)
        self.assertTrue(result['route_match'])
        self.assertTrue(result['target_proven'])
        self.assertEqual(result['probe_status'], 'reachable')
        self.assertIn('-p 2022', proxy.execute.call_args_list[1][0][0])
        self.assertEqual(
            file_utils.from_device.return_value.copyfile.call_args.kwargs[
                'source'],
            'http://user:pass@192.0.2.1:2000/test.txt')

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
        url = 'ftp://user:pass@1.1.1.1/path/file.bin'
        proxied_url = 'ftp://user:pass@proxy.host:2000/path/file.bin'
        fu.validate_and_update_url = Mock(return_value=url)
        fu.stat = Mock(side_effect=FileNotFoundError(
            f'not found: {proxied_url}'
        ))

        with self.assertRaises(FileNotFoundError) as context:
            get_file_size_from_server(device=device,
                                      server='1.1.1.1',
                                      path='path/file.bin',
                                      protocol='ftp',
                                      timeout=10,
                                      fu_session=fu)

        proxy_dev.api.stop_socat_relay.assert_called_once_with('1234')
        self.assertNotIn('user', str(context.exception))
        self.assertNotIn('pass', str(context.exception))
        self.assertIn(
            'not found: ftp://****:****@proxy.host:2000/path/file.bin',
            str(context.exception),
        )

    def test_get_file_size_from_server_via_proxy_redacts_stat_error(self):
        device = MagicMock()
        device.api.get_proxy = Mock(return_value='js')
        device.api.convert_server_to_linux_device = Mock(return_value=None)

        proxy_dev = MagicMock()
        proxy_dev.api.start_socat_relay = Mock(return_value=(4321, '1234'))
        proxy_dev.api.stop_socat_relay = Mock()
        device.testbed.devices = {'js': proxy_dev}

        fu = MagicMock()
        fu.get_hostname = Mock(return_value='proxy.example')
        url = 'https://user:p%40ssword@server.example/path/file.bin'
        proxied_url = 'https://user:p%40ssword@proxy.example:4321/path/file.bin'
        fu.validate_and_update_url = Mock(return_value=url)
        fu.stat = Mock(side_effect=Exception(
            f'Failed to retrieve {proxied_url}'
        ))

        with self.assertRaises(Exception) as context:
            get_file_size_from_server(
                device=device,
                server='server.example',
                path='path/file.bin',
                protocol='https',
                timeout=10,
                fu_session=fu,
            )

        fu.stat.assert_called_once_with(
            target=proxied_url,
            timeout_seconds=10,
        )
        proxy_dev.api.stop_socat_relay.assert_called_once_with('1234')
        self.assertNotIn('user', str(context.exception))
        self.assertNotIn('p%40ssword', str(context.exception))
        self.assertIn(
            'https://****:****@proxy.example:4321/path/file.bin',
            str(context.exception),
        )
        self.assertTrue(context.exception.__suppress_context__)

    def test_get_file_size_from_server_via_proxy_redacts_not_implemented_error(self):
        device = MagicMock()
        device.api.get_proxy = Mock(return_value='js')
        device.api.convert_server_to_linux_device = Mock(return_value=None)

        proxy_dev = MagicMock()
        proxy_dev.api.start_socat_relay = Mock(return_value=(4321, '1234'))
        proxy_dev.api.stop_socat_relay = Mock()
        device.testbed.devices = {'js': proxy_dev}

        fu = MagicMock()
        fu.get_hostname = Mock(return_value='proxy.example')
        url = 'https://user:p%40ssword@server.example/path/file.bin'
        proxied_url = 'https://user:p%40ssword@proxy.example:4321/path/file.bin'
        fu.validate_and_update_url = Mock(return_value=url)
        fu.stat = Mock(side_effect=NotImplementedError(
            f'Unsupported URL: {proxied_url}'
        ))

        with self.assertRaises(NotImplementedError) as context:
            get_file_size_from_server(
                device=device,
                server='server.example',
                path='path/file.bin',
                protocol='https',
                timeout=10,
                fu_session=fu,
            )

        proxy_dev.api.stop_socat_relay.assert_called_once_with('1234')
        self.assertNotIn('user', str(context.exception))
        self.assertNotIn('p%40ssword', str(context.exception))
        self.assertTrue(context.exception.__suppress_context__)

    def test_get_file_size_from_server_via_proxy_stops_relay_on_url_error(self):
        device = MagicMock()
        device.api.get_proxy = Mock(return_value='js')
        device.api.convert_server_to_linux_device = Mock(return_value=None)

        proxy_dev = MagicMock()
        proxy_dev.api.start_socat_relay = Mock(return_value=(4321, '1234'))
        proxy_dev.api.stop_socat_relay = Mock()
        device.testbed.devices = {'js': proxy_dev}

        fu = MagicMock()
        url = 'https://user:p%40ssword@server.example/path/file.bin'
        fu.get_hostname = Mock(side_effect=Exception(
            f'Unable to build proxy URL: {url}'
        ))
        fu.validate_and_update_url = Mock(return_value=url)
        fu.stat = Mock()

        with self.assertRaises(Exception) as context:
            get_file_size_from_server(
                device=device,
                server='server.example',
                path='path/file.bin',
                protocol='https',
                timeout=10,
                fu_session=fu,
            )

        fu.stat.assert_not_called()
        proxy_dev.api.stop_socat_relay.assert_called_once_with('1234')
        self.assertNotIn('user', str(context.exception))
        self.assertNotIn('p%40ssword', str(context.exception))
        self.assertTrue(context.exception.__suppress_context__)

    def test_get_file_size_from_server_via_proxy_redacts_invalid_url(self):
        device = MagicMock()
        device.api.get_proxy = Mock(return_value='js')
        device.api.convert_server_to_linux_device = Mock(return_value=None)

        proxy_dev = MagicMock()
        device.testbed.devices = {'js': proxy_dev}

        fu = MagicMock()
        fu.validate_and_update_url = Mock(
            return_value='https://user:password@/path/file.bin'
        )

        with self.assertRaises(Exception) as context:
            get_file_size_from_server(
                device=device,
                server='server.example',
                path='path/file.bin',
                protocol='https',
                timeout=10,
                fu_session=fu,
            )

        self.assertNotIn('user', str(context.exception))
        self.assertNotIn('password', str(context.exception))
        self.assertIn(
            'https://****:****@/path/file.bin',
            str(context.exception),
        )

    def test_get_file_size_from_server_redacts_credentials_from_error(self):
        device = MagicMock()
        device.api.get_proxy = Mock(return_value=None)

        fu = MagicMock()
        url = 'https://user:p%40ssword@server.example/path/file.bin'
        fu.validate_and_update_url = Mock(return_value=url)
        fu.stat = Mock(side_effect=Exception(
            f'Failed to retrieve {url}'
        ))

        with self.assertRaises(Exception) as context:
            get_file_size_from_server(
                device=device,
                server='server.example',
                path='path/file.bin',
                protocol='https',
                timeout=10,
                fu_session=fu,
            )

        fu.stat.assert_called_once_with(
            target=url,
            timeout_seconds=10,
        )
        fu.validate_and_update_url.assert_called_once_with(
            'https://server.example/path/file.bin', device=device)
        self.assertNotIn('user', str(context.exception))
        self.assertNotIn('p%40ssword', str(context.exception))
        self.assertIn(
            'https://****:****@server.example/path/file.bin',
            str(context.exception),
        )
        self.assertTrue(context.exception.__suppress_context__)

    def test_get_file_size_from_server_redacts_file_not_found_error(self):
        device = MagicMock()
        device.api.get_proxy = Mock(return_value=None)

        fu = MagicMock()
        url = 'https://user:p%40ssword@server.example/path/file.bin'
        fu.validate_and_update_url = Mock(return_value=url)
        fu.stat = Mock(side_effect=FileNotFoundError(
            f'not found: {url}'
        ))

        with self.assertRaises(FileNotFoundError) as context:
            get_file_size_from_server(
                device=device,
                server='server.example',
                path='path/file.bin',
                protocol='https',
                timeout=10,
                fu_session=fu,
            )

        self.assertNotIn('user', str(context.exception))
        self.assertNotIn('p%40ssword', str(context.exception))
        self.assertIn(
            'not found: https://****:****@server.example/path/file.bin',
            str(context.exception),
        )
        self.assertTrue(context.exception.__suppress_context__)

    def test_get_file_size_from_server_redacts_not_implemented_error(self):
        device = MagicMock()
        device.api.get_proxy = Mock(return_value=None)

        fu = MagicMock()
        url = 'https://user:p%40ssword@server.example/path/file.bin'
        fu.validate_and_update_url = Mock(return_value=url)
        fu.stat = Mock(side_effect=NotImplementedError(
            f'unsupported URL: {url}'
        ))

        with self.assertRaises(NotImplementedError) as context:
            get_file_size_from_server(
                device=device,
                server='server.example',
                path='path/file.bin',
                protocol='https',
                timeout=10,
                fu_session=fu,
            )

        self.assertNotIn('user', str(context.exception))
        self.assertNotIn('p%40ssword', str(context.exception))
        self.assertIn(
            'unsupported URL: https://****:****@server.example/path/file.bin',
            str(context.exception),
        )
        self.assertTrue(context.exception.__suppress_context__)

    def test_get_file_size_from_server_detects_case_insensitive_not_found(self):
        device = MagicMock()
        device.api.get_proxy = Mock(return_value=None)

        fu = MagicMock()
        url = 'https://user:p%40ssword@server.example/path/file.bin'
        fu.validate_and_update_url = Mock(return_value=url)
        fu.stat = Mock(side_effect=Exception(
            f'FILE NOT FOUND: {url}'
        ))

        with self.assertRaises(FileNotFoundError) as context:
            get_file_size_from_server(
                device=device,
                server='server.example',
                path='path/file.bin',
                protocol='https',
                timeout=10,
                fu_session=fu,
            )

        self.assertNotIn('user', str(context.exception))
        self.assertNotIn('p%40ssword', str(context.exception))
        self.assertIn(
            'FILE NOT FOUND: https://****:****@server.example/path/file.bin',
            str(context.exception),
        )
        self.assertTrue(context.exception.__suppress_context__)

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
