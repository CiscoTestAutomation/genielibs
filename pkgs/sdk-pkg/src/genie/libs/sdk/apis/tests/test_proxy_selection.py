"""Unit tests for generic runtime proxy selection."""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from genie.libs.sdk.apis.proxy_selection import (
    clear_runtime_proxy_cache,
    invalidate_runtime_proxy_cache,
    runtime_proxy_candidates,
    select_runtime_proxy_for_device,
)
from genie.libs.sdk.apis.utils import probe_tcp_from_server


class Proxy:
    def __init__(self, connect_error=None, execute=None):
        self.connected = False
        self.connect_error = connect_error
        self.connect_calls = 0
        self.disconnect_calls = 0
        self.execute = execute

    def is_connected(self):
        return self.connected

    def connect(self):
        self.connect_calls += 1
        if self.connect_error:
            raise self.connect_error
        self.connected = True

    def disconnect(self):
        self.disconnect_calls += 1
        self.connected = False


def server(subnet, interface_ip, family='ipv4', rack=None, row=None,
           proxy_service=False):
    data = {
        'management': {'routes': {family: [
            {'subnet': subnet, 'interface': 'eth0'}]}},
        'interfaces': {'eth0': {family: interface_ip}},
    }
    if rack or row:
        data['custom'] = {'rack': rack, 'row': row}
    if proxy_service:
        data['services'] = {'ssh': {
            'application': 'proxy', 'protocol': 'ssh', 'port': 22,
            'order': 1}}
    return data


def device(candidates, proxies, addresses=None, servers=None,
           target_probe=False, global_candidates=False, connections=None,
           custom=None):
    selection = {
        'mode': 'runtime', 'target_probe': target_probe, 'timeout': 3}
    device_custom = dict(custom or {})
    if global_candidates:
        selection['candidates'] = candidates
    else:
        device_custom['proxy_selection'] = {'candidates': candidates}
    testbed = SimpleNamespace(
        custom={'proxy_selection': selection},
        servers=servers or {}, devices=proxies)
    api = SimpleNamespace(
        convert_server_to_linux_device=lambda name: proxies.get(name),
        probe_tcp_from_server=Mock())
    return SimpleNamespace(
        name='router', testbed=testbed, api=api,
        custom=device_custom,
        management={'address': addresses or {'ipv4': '10.20.1.5/24'}},
        connections=connections or {}, via=None)


class TestRuntimeProxySelection(unittest.TestCase):

    def test_longest_prefix_and_deterministic_tie(self):
        proxies = {name: Proxy() for name in ('broad', 'first', 'second')}
        dut = device(
            ['broad', 'first', 'second'], proxies,
            servers={
                'broad': server('10.0.0.0/8', '192.0.2.1/24'),
                'first': server('10.20.0.0/16', '192.0.2.2/24'),
                'second': server('10.20.0.0/16', '192.0.2.3/24'),
            })

        result = select_runtime_proxy_for_device(dut)

        self.assertEqual(result['server_name'], 'first')
        self.assertEqual(result['route']['prefix_length'], 16)
        self.assertEqual({key: result[key] for key in (
            'server_name', 'device_ip', 'target_port', 'subnet',
            'interface', 'route_match', 'connected', 'target_proven',
            'probe_status', 'cache_hit', 'reason')}, {
                'server_name': 'first', 'device_ip': '10.20.1.5',
                'target_port': 22, 'subnet': '10.20.0.0/16',
                'interface': 'eth0', 'route_match': True,
                'connected': True, 'target_proven': False,
                'probe_status': 'not_requested', 'cache_hit': False,
                'reason': 'route_match',
        })
        self.assertEqual(proxies['first'].connect_calls, 1)
        self.assertEqual(proxies['broad'].connect_calls, 0)

    def test_ipv6_route(self):
        proxies = {'v6': Proxy()}
        dut = device(
            ['v6'], proxies,
            addresses={'ipv6': ['2001:db8:10::9/64']},
            servers={'v6': server(
                '2001:db8:10::/64', '2001:db8:ffff::1/64', 'ipv6')})

        result = select_runtime_proxy_for_device(dut)

        self.assertEqual(result['server_name'], 'v6')
        self.assertEqual(result['device_ip'], '2001:db8:10::9')

    def test_dual_stack_uses_management_address_order_between_families(self):
        proxies = {'v4': Proxy(), 'v6': Proxy()}
        dut = device(
            ['v4', 'v6'], proxies,
            addresses={
                'ipv4': ['10.20.1.5/24'],
                'ipv6': ['2001:db8:10::9/64'],
            },
            servers={
                'v4': server('10.0.0.0/8', '192.0.2.1/24'),
                'v6': server(
                    '2001:db8:10::/64', '2001:db8:ffff::1/64', 'ipv6'),
            })

        result = select_runtime_proxy_for_device(dut)

        self.assertEqual(result['server_name'], 'v4')
        self.assertEqual(result['device_ip'], '10.20.1.5')

    def test_connection_failure_falls_through(self):
        proxies = {
            'bad': Proxy(RuntimeError('refused')),
            'good': Proxy(),
        }
        dut = device(['bad', 'good'], proxies)

        result = select_runtime_proxy_for_device(dut)

        self.assertEqual(result['server_name'], 'good')
        self.assertIn('connection failed', result['failures'][0])

    def test_any_management_address_can_prove_candidate(self):
        proxy = Proxy()
        dut = device(
            ['proxy'], {'proxy': proxy},
            addresses={'ipv4': ['10.0.0.9/24', '10.1.0.9/24']},
            target_probe=True)

        def probe(server, hosts, port, timeout):
            server.connect()
            return [
                {'host': hosts[0], 'reachable': False,
                 'status': 'unreachable'},
                {'host': hosts[1], 'reachable': True,
                 'status': 'reachable'},
            ]
        dut.api.probe_tcp_from_server.side_effect = probe

        result = select_runtime_proxy_for_device(dut)

        self.assertEqual(result['server_name'], 'proxy')
        self.assertEqual(result['device_ip'], '10.1.0.9')
        self.assertTrue(result['target_proven'])
        self.assertEqual(result['probe_status'], 'reachable')
        self.assertEqual(result['reason'], 'target_proven')
        dut.api.probe_tcp_from_server.assert_called_once_with(
            proxy, ['10.0.0.9', '10.1.0.9'], 22, timeout=3.0)

    def test_unavailable_tool_is_fallback_not_immediate_selection(self):
        proxies = {'fallback': Proxy(), 'proven': Proxy()}
        dut = device(
            ['fallback', 'proven'], proxies, target_probe=True)

        def probe(server, hosts, port, timeout):
            server.connect()
            return [{
                'host': hosts[0],
                'reachable': server is proxies['proven'],
                'status': ('reachable' if server is proxies['proven']
                           else 'unavailable'),
            }]
        dut.api.probe_tcp_from_server.side_effect = probe

        result = select_runtime_proxy_for_device(dut)

        self.assertEqual(result['server_name'], 'proven')
        self.assertEqual(proxies['fallback'].disconnect_calls, 1)

    def test_cache_hit_requires_live_connection_and_clear_is_explicit(self):
        proxy = Proxy()
        dut = device(['proxy'], {'proxy': proxy})

        first = select_runtime_proxy_for_device(dut)
        second = select_runtime_proxy_for_device(dut)
        proxy.connected = False
        third = select_runtime_proxy_for_device(dut)
        clear_runtime_proxy_cache(dut)
        fourth = select_runtime_proxy_for_device(dut)

        self.assertFalse(first['cache_hit'])
        self.assertTrue(second['cache_hit'])
        self.assertFalse(third['cache_hit'])
        self.assertFalse(fourth['cache_hit'])
        self.assertEqual(proxy.connect_calls, 2)

    def test_cache_hit_skips_route_lookup_and_logs_consolidated_decision(self):
        proxy = Proxy()
        dut = device(
            ['proxy'], {'proxy': proxy},
            servers={'proxy': server(
                '10.20.0.0/16', '192.0.2.1/24')})

        with self.assertLogs(level='INFO') as logs:
            select_runtime_proxy_for_device(dut)
            select_runtime_proxy_for_device(dut)

        self.assertEqual(logs.output, [
            'INFO:genie.libs.sdk.apis.server_route_lookup:Find server IP for '
            'device IP: searching 1 server(s) for route covering device IP '
            '10.20.1.5',
            'INFO:genie.libs.sdk.apis.server_route_lookup:Find server IP for '
            "device IP: best match is server 'proxy' interface IP "
            '192.0.2.1 (prefix_len=16) for device 10.20.1.5',
            'INFO:genie.libs.sdk.apis.proxy_selection:Runtime proxy decision '
            'device=router cache=miss selected_server=proxy '
            'management_ip=10.20.1.5 subnet=10.20.0.0/16 interface=eth0 '
            'connection=connected probe=not_requested reason=route_match',
            'INFO:genie.libs.sdk.apis.proxy_selection:Runtime proxy decision '
            'device=router cache=hit selected_server=proxy '
            'management_ip=10.20.1.5 subnet=10.20.0.0/16 interface=eth0 '
            'connection=connected probe=not_requested reason=route_match',
        ])

    def test_fallback_decision_logs_reason(self):
        proxy = Proxy()
        dut = device(
            ['proxy'], {'proxy': proxy}, servers={'proxy': {}})

        with self.assertLogs(
                'genie.libs.sdk.apis.proxy_selection', level='INFO') as logs:
            select_runtime_proxy_for_device(dut)

        self.assertEqual(logs.output, [
            'INFO:genie.libs.sdk.apis.proxy_selection:Runtime proxy decision '
            'device=router cache=miss selected_server=proxy '
            'management_ip=10.20.1.5 subnet=None interface=None '
            'connection=connected probe=not_requested reason=fallback',
        ])

    def test_negative_cache_and_metadata_invalidation(self):
        proxy = Proxy(RuntimeError('refused'))
        servers = {'bad': {'address': '192.0.2.10'}}
        dut = device(['bad'], {'bad': proxy}, servers=servers)

        with patch(
                'genie.libs.sdk.apis.utils.'
                'find_server_route_for_device_ip', return_value=None) as route:
            self.assertIsNone(select_runtime_proxy_for_device(dut))
            self.assertIsNone(select_runtime_proxy_for_device(dut))
            self.assertEqual(route.call_count, 1)
            self.assertEqual(proxy.connect_calls, 1)

            servers['bad']['address'] = '192.0.2.11'
            self.assertIsNone(select_runtime_proxy_for_device(dut))
            self.assertEqual(route.call_count, 2)

        self.assertEqual(proxy.connect_calls, 2)

    def test_invalidated_selection_tries_next_candidate(self):
        proxies = {'first': Proxy(), 'second': Proxy()}
        dut = device(['first', 'second'], proxies)

        first = select_runtime_proxy_for_device(dut)
        self.assertTrue(invalidate_runtime_proxy_cache(
            dut, 'first', 'relay failed'))
        second = select_runtime_proxy_for_device(dut)

        self.assertEqual(first['server_name'], 'first')
        self.assertEqual(second['server_name'], 'second')
        self.assertIn('first: relay failed', second['failures'])

    def test_server_metadata_and_rack_discovery(self):
        proxies = {'rack-proxy': Proxy(), 'other': Proxy()}
        servers = {
            'other': server(
                '192.0.2.0/24', '192.0.2.1/24', proxy_service=True),
            'rack-proxy': server(
                '198.51.100.0/24', '198.51.100.1/24', rack='rack-a',
                proxy_service=True),
        }
        dut = device([], proxies, servers=servers, custom={'rack': 'rack-a'})

        self.assertEqual(
            runtime_proxy_candidates(dut), ['other', 'rack-proxy'])
        result = select_runtime_proxy_for_device(dut)

        self.assertEqual(result['server_name'], 'rack-proxy')
        self.assertEqual(result['reason'], 'fallback')

    def test_global_candidate_without_route_does_not_override_current(self):
        proxies = {'global': Proxy(), 'current': Proxy()}
        dut = device(
            ['global'], proxies, global_candidates=True,
            servers={
                'global': server(
                    '192.0.2.0/24', '192.0.2.1/24', proxy_service=True),
                'current': {'address': '198.51.100.10'},
            })

        result = select_runtime_proxy_for_device(
            dut, fallback_proxy='current')

        self.assertEqual(result['server_name'], 'current')
        self.assertEqual(proxies['global'].connect_calls, 0)

    def test_devices_only_current_fallback_precedes_unrouted_candidate(self):
        proxies = {'global': Proxy(), 'current': Proxy()}
        dut = device(
            ['global'], proxies, global_candidates=True,
            servers={
                'global': server(
                    '192.0.2.0/24', '192.0.2.1/24', proxy_service=True),
            })

        result = select_runtime_proxy_for_device(
            dut, fallback_proxy='current')

        self.assertEqual(result['server_name'], 'current')
        self.assertEqual(proxies['current'].connect_calls, 1)
        self.assertEqual(proxies['global'].connect_calls, 0)

    def test_no_route_tries_remaining_configured_not_discovered_metadata(self):
        proxies = {
            'proxy-a': Proxy(RuntimeError('refused')),
            'proxy-b': Proxy(),
            'metadata-only': Proxy(),
        }
        dut = device(
            ['proxy-a', 'proxy-b'], proxies, global_candidates=True,
            servers={
                'proxy-a': {'address': '192.0.2.10'},
                'proxy-b': {'address': '192.0.2.11'},
                'metadata-only': server(
                    '198.51.100.0/24', '198.51.100.1/24',
                    proxy_service=True),
            })

        result = select_runtime_proxy_for_device(
            dut, fallback_proxy='proxy-a')

        self.assertEqual(result['server_name'], 'proxy-b')
        self.assertEqual(proxies['proxy-a'].connect_calls, 1)
        self.assertEqual(proxies['proxy-b'].connect_calls, 1)
        self.assertEqual(proxies['metadata-only'].connect_calls, 0)

    def test_real_route_and_probe_helpers_use_target_connection_port(self):
        execute = Mock(side_effect=[
            '/usr/bin/nmap',
            ('Host: 10.20.1.5 ()\tPorts: '
             '2022/open/tcp//ssh///\n__GENIE_NMAP_RC__=0\n'),
        ])
        proxy = Proxy(execute=execute)
        proxy_server = server('10.20.0.0/16', '192.0.2.1/24')
        proxy_server['services'] = {
            'later': {
                'application': 'proxy', 'protocol': 'ssh',
                'port': 2202, 'order': 2},
            'first': {
                'application': 'proxy', 'protocol': 'ssh',
                'port': 2201, 'order': 1},
        }
        dut = device(
            ['proxy'], {'proxy': proxy}, target_probe=True,
            servers={'proxy': proxy_server},
            connections={
                'https': {'protocol': 'https', 'port': 443},
                'cli': {'protocol': 'ssh', 'port': 2022},
            })
        dut.via = 'cli'
        dut.api.probe_tcp_from_server = lambda remote, hosts, port, timeout: \
            probe_tcp_from_server(
                dut, remote, hosts, port, timeout=timeout)

        result = select_runtime_proxy_for_device(dut)

        self.assertTrue(result['target_proven'])
        self.assertEqual(result['target_port'], 2022)
        self.assertIn('-p 2022', execute.call_args_list[1][0][0])

    def test_non_ssh_via_uses_ssh_protocol_connection_port(self):
        proxy = Proxy()
        dut = device(
            ['proxy'], {'proxy': proxy},
            connections={
                'https': {'protocol': 'https', 'port': 443},
                'cli': {'protocol': 'ssh', 'port': 2022},
            })
        dut.via = 'https'

        result = select_runtime_proxy_for_device(dut)

        self.assertEqual(result['target_port'], 2022)

    def test_disabled_mode_does_not_resolve_candidates(self):
        proxy = Proxy()
        dut = device(['proxy'], {'proxy': proxy})
        dut.testbed.custom['proxy_selection']['mode'] = 'static'

        self.assertIsNone(select_runtime_proxy_for_device(dut))
        self.assertEqual(proxy.connect_calls, 0)


if __name__ == '__main__':
    unittest.main()
