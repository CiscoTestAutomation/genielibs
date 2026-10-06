"""Unit tests for the IOSXR routing configure/get APIs."""

import unittest
from unittest.mock import MagicMock

from genie.libs.sdk.apis.iosxr.routing.configure import (
    build_static_routing_route_config,
    configure_static_routing_route,
    unconfigure_static_routing_route,
)
from genie.libs.sdk.apis.iosxr.routing.get import (
    get_routing_address_family,
    get_routing_route_next_hop,
)
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestBuildStaticRoutingRouteConfig(unittest.TestCase):

    def test_default_vrf_ipv4(self):
        self.assertEqual(
            build_static_routing_route_config('203.0.113.10/32', '192.0.2.1'),
            ['router static',
             ' address-family ipv4 unicast',
             '  203.0.113.10/32 192.0.2.1'])

    def test_non_default_vrf_ipv6(self):
        self.assertEqual(
            build_static_routing_route_config('2001:db8::10/128',
                                              '2001:db8:1::1',
                                              address_family='ipv6',
                                              vrf='Mgmt-vrf'),
            ['router static',
             ' vrf Mgmt-vrf',
             '  address-family ipv6 unicast',
             '   2001:db8::10/128 2001:db8:1::1'])

    def test_unconfigure(self):
        self.assertEqual(
            build_static_routing_route_config('203.0.113.10/32',
                                              '192.0.2.1',
                                              unconfigure=True),
            ['router static',
             ' address-family ipv4 unicast',
             '  no 203.0.113.10/32 192.0.2.1'])

    def test_invalid_address_family(self):
        with self.assertRaises(ValueError):
            build_static_routing_route_config('203.0.113.10/32', '192.0.2.1',
                                              address_family='ipv5')


class TestConfigureStaticRoutingRoute(unittest.TestCase):

    def test_configure(self):
        device = MagicMock()
        config = configure_static_routing_route(device, '203.0.113.10/32',
                                                '192.0.2.1', vrf='Mgmt-vrf')
        device.configure.assert_called_once_with(config)
        self.assertIn('  address-family ipv4 unicast', config)

    def test_unconfigure(self):
        device = MagicMock()
        config = unconfigure_static_routing_route(device, '203.0.113.10/32',
                                                  '192.0.2.1')
        device.configure.assert_called_once_with(config)
        self.assertEqual(config[-1], '  no 203.0.113.10/32 192.0.2.1')


class TestGetRoutingAddressFamily(unittest.TestCase):

    def test_ipv4(self):
        self.assertEqual(get_routing_address_family('10.1.1.1'), 'ipv4')

    def test_ipv6_with_prefix(self):
        self.assertEqual(get_routing_address_family('2001:db8::1/128'), 'ipv6')

    def test_invalid(self):
        with self.assertRaises(ValueError):
            get_routing_address_family('not-an-ip')


class TestGetRoutingRouteNextHop(unittest.TestCase):

    PARSED = {
        'vrf': {
            'default': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.1.1.0/24': {
                                'route': '10.1.1.0/24',
                                'active': True,
                                'known_via': 'static',
                                'source_protocol': 'static',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {'index': 1,
                                            'next_hop': '192.0.2.1'},
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    def test_next_hop_found(self):
        device = MagicMock()
        device.parse.return_value = _Parsed(self.PARSED)
        result = get_routing_route_next_hop(device, '10.1.1.1', vrf='Mgmt-vrf')
        device.parse.assert_called_once_with(
            'show route vrf Mgmt-vrf ipv4 10.1.1.1')
        self.assertEqual(result['next_hops'], ['192.0.2.1'])
        self.assertFalse(result['connected'])
        self.assertEqual(result['known_via'], 'static')

    def test_command_without_vrf(self):
        device = MagicMock()
        device.parse.return_value = _Parsed(self.PARSED)
        get_routing_route_next_hop(device, '10.1.1.1')
        device.parse.assert_called_once_with('show route ipv4 10.1.1.1')

    def test_empty_parser_output_returns_none(self):
        # SchemaEmptyParserError means the device answered and simply has
        # no route ('% Network not in table'), which is a real 'no route'.
        device = MagicMock()
        device.parse.side_effect = SchemaEmptyParserError('empty')
        self.assertIsNone(get_routing_route_next_hop(device, '10.1.1.1'))

    def test_unexpected_parse_failure_propagates(self):
        # Anything other than an empty parse leaves reachability unknown and
        # must not be disguised as 'no route'.
        device = MagicMock()
        device.parse.side_effect = Exception('boom')
        with self.assertRaises(Exception) as raised:
            get_routing_route_next_hop(device, '10.1.1.1')
        self.assertEqual(str(raised.exception), 'boom')

    def test_invalid_route_raises_value_error(self):
        # A malformed address is a caller error, not an answer about
        # reachability, so it is raised rather than reported as 'no route'.
        device = MagicMock()
        with self.assertRaises(ValueError):
            get_routing_route_next_hop(device, 'not-an-ip')
        device.parse.assert_not_called()

    def test_explicit_address_family_skips_validation(self):
        # The address family is only derived from the route when the caller
        # does not supply one, so an explicit value bypasses the check.
        device = MagicMock()
        device.parse.return_value = _Parsed(self.PARSED)
        get_routing_route_next_hop(device, '10.1.1.0/24',
                                   address_family='ipv4')
        device.parse.assert_called_once_with('show route ipv4 10.1.1.0/24')


class _Parsed(dict):
    """Minimal stand-in exposing the Dq ``.q`` interface used by the API."""

    @property
    def q(self):
        from genie.utils import Dq
        return Dq(self)


if __name__ == '__main__':
    unittest.main()
