"""Unit tests for the IOSXR temporary transfer route feature."""

import unittest
from unittest.mock import MagicMock, call

from genie.libs.filetransferutils.plugins.iosxr.fileutils import FileUtils
from genie.libs.filetransferutils.plugins.iosxr.https.fileutils import (
    FileUtils as HttpsFileUtils)
from genie.libs.sdk.apis.iosxr.routing.get import get_routing_route_next_hop
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq


def make_device(gateway=None, next_hops=None, name='xr1', routes=None):
    device = MagicMock()
    device.name = name
    device.device = device
    management = {}
    if gateway:
        management['gateway'] = gateway
    if routes:
        management['routes'] = routes
    device.management = management
    if next_hops is None:
        device.api.get_routing_route_next_hop.return_value = None
    else:
        device.api.get_routing_route_next_hop.return_value = {
            'route': '10.1.1.1/32',
            'next_hops': next_hops,
            'outgoing_interfaces': [],
            'known_via': 'static',
            'source_protocol': 'static',
            'connected': False,
        }
    return device


class _QDict(dict):
    """dict with the ``.q`` Dq accessor that parser output provides."""

    @property
    def q(self):
        return Dq(self)


def make_fileutils():
    """Return an un-initialised IOSXR ``FileUtils`` instance.

    ``FileUtilsBase.__new__`` is an abstraction factory: called without
    ``os``/``protocol`` it re-resolves ``cls`` through ``Lookup`` and
    returns the generic ``FileUtils``, which has none of the IOSXR
    temporary transfer route methods. Going straight to ``object.__new__``
    keeps the concrete IOSXR class while still skipping ``__init__``, which
    would otherwise require a testbed and a live connection.
    """
    return object.__new__(FileUtils)


def make_https_fileutils():
    """Return an un-initialised IOSXR HTTPS ``FileUtils`` instance.

    The clock / certificate / DNS / trustpoint setup lives on
    ``HTTPFileUtilsBase``, which only the ``iosxr.https`` plugin mixes in
    alongside the IOSXR temporary transfer route methods. Tests that need
    that setup path must use this class rather than the plain IOSXR one.
    """
    return object.__new__(HttpsFileUtils)


class TestTransferEndpointIp(unittest.TestCase):

    def setUp(self):
        self.fu = make_fileutils()

    def test_ipv4_remote_destination(self):
        self.assertEqual(
            self.fu._get_transfer_endpoint_ip('flash:/a.bin',
                                              'scp://1.2.3.4//tmp/a.bin'),
            '1.2.3.4')

    def test_ipv4_remote_source(self):
        self.assertEqual(
            self.fu._get_transfer_endpoint_ip('http://1.2.3.4/a.bin',
                                              'flash:/a.bin'),
            '1.2.3.4')

    def test_https_endpoint(self):
        self.assertEqual(
            self.fu._get_transfer_endpoint_ip('flash:/a.bin',
                                              'https://1.2.3.4:8443/a.bin'),
            '1.2.3.4')

    def test_ipv6_endpoint(self):
        self.assertEqual(
            self.fu._get_transfer_endpoint_ip('flash:/a.bin',
                                              'scp://[2001:db8::10]//tmp/a.bin'),
            '2001:db8::10')

    def test_device_local_only(self):
        self.assertIsNone(
            self.fu._get_transfer_endpoint_ip('flash:/a.bin',
                                              'harddisk:/a.bin'))

    def test_device_local_disk_schemes(self):
        for local in ('disk0:/a.bin', 'disk0a:/a.bin', 'disk2:/a.bin',
                      'apphost:/a.bin', 'running-config', 'startup-config'):
            with self.subTest(local=local):
                self.assertIsNone(
                    self.fu._get_transfer_endpoint_ip('flash:/a.bin', local))

    def test_dns_hostname_is_skipped(self):
        self.assertIsNone(
            self.fu._get_transfer_endpoint_ip('flash:/a.bin',
                                              'scp://server.example.com//a.bin'))


class TestManagementGateway(unittest.TestCase):

    def setUp(self):
        self.fu = make_fileutils()

    def test_ipv4_gateway(self):
        device = make_device(gateway={'ipv4': '192.0.2.1'})
        self.assertEqual(self.fu._get_management_gateway(device, 'ipv4'),
                         '192.0.2.1')

    def test_ipv6_gateway_list(self):
        device = make_device(gateway={'ipv6': ['2001:db8:1::1']})
        self.assertEqual(self.fu._get_management_gateway(device, 'ipv6'),
                         '2001:db8:1::1')

    def test_gateway_prefix_is_stripped(self):
        device = make_device(gateway={'ipv4': '192.0.2.1/24'})
        self.assertEqual(self.fu._get_management_gateway(device, 'ipv4'),
                         '192.0.2.1')

    def test_no_gateway(self):
        device = make_device()
        self.assertIsNone(self.fu._get_management_gateway(device, 'ipv4'))

    def test_wrong_family(self):
        device = make_device(gateway={'ipv4': '192.0.2.1'})
        self.assertIsNone(self.fu._get_management_gateway(device, 'ipv6'))


class TestEnsureTemporaryTransferRoute(unittest.TestCase):

    def setUp(self):
        self.fu = make_fileutils()

    def _add(self, device, **kwargs):
        params = dict(source='flash:/a.bin',
                      destination='scp://1.2.3.4//tmp/a.bin',
                      vrf='Mgmt-vrf',
                      jit_route=True)
        params.update(kwargs)
        return self.fu._ensure_temporary_transfer_route(device=device,
                                                        **params)

    def test_legacy_jit_route_flag_is_ignored(self):
        # Temporary transfer routing is the default behaviour for IOSXR;
        # the legacy ``jit_route`` opt-in flag no longer suppresses it.
        device = make_device(gateway={'ipv4': '192.0.2.1'})
        temporary_route = self._add(device, jit_route=False)
        self.assertEqual(
            temporary_route,
            {'prefix': '1.2.3.4/32', 'next_hop': '192.0.2.1',
             'address_family': 'ipv4', 'vrf': 'Mgmt-vrf'})
        device.api.configure_static_routing_route.assert_called_once_with(
            prefix='1.2.3.4/32', next_hop='192.0.2.1',
            address_family='ipv4', vrf='Mgmt-vrf')

    def test_default_vrf_used_when_vrf_absent(self):
        device = make_device(gateway={'ipv4': '192.0.2.1'})
        temporary_route = self._add(device, vrf=None)
        self.assertEqual(
            temporary_route,
            {'prefix': '1.2.3.4/32', 'next_hop': '192.0.2.1',
             'address_family': 'ipv4', 'vrf': None})
        device.api.get_routing_route_next_hop.assert_called_once_with(
            route='1.2.3.4', address_family='ipv4', vrf=None)
        device.api.configure_static_routing_route.assert_called_once_with(
            prefix='1.2.3.4/32', next_hop='192.0.2.1',
            address_family='ipv4', vrf=None)

    def test_noop_for_device_local_transfer(self):
        device = make_device(gateway={'ipv4': '192.0.2.1'})
        self.assertIsNone(self._add(device, destination='harddisk:/a.bin'))
        device.api.configure_static_routing_route.assert_not_called()

    def test_noop_without_gateway(self):
        device = make_device()
        self.assertIsNone(self._add(device))
        device.api.configure_static_routing_route.assert_not_called()

    def test_noop_when_route_already_uses_gateway(self):
        device = make_device(gateway={'ipv4': '192.0.2.1'},
                             next_hops=['192.0.2.1'])
        self.assertIsNone(self._add(device))
        device.api.configure_static_routing_route.assert_not_called()

    def test_noop_when_live_next_hop_is_equivalent_ipv6_spelling(self):
        # The device renders IPv6 next hops in its own canonical form, so a
        # live next hop of '2001:db8:1::1' is the same address as a testbed
        # gateway written '2001:0db8:1:0::1'. The guard must normalise both
        # sides rather than compare raw strings, otherwise a redundant host
        # route is installed over a path that already uses the gateway.
        device = make_device(gateway={'ipv6': ['2001:0db8:1:0::1']},
                             next_hops=['2001:db8:1::1'])
        self.assertIsNone(
            self._add(device,
                      destination='scp://[2001:db8::10]//tmp/a.bin'))
        device.api.configure_static_routing_route.assert_not_called()

    def test_noop_when_live_next_hop_carries_prefix_length(self):
        # A next hop reported with a prefix length names the same address as
        # the bare gateway.
        device = make_device(gateway={'ipv4': '192.0.2.1'},
                             next_hops=['192.0.2.1/24'])
        self.assertIsNone(self._add(device))
        device.api.configure_static_routing_route.assert_not_called()

    def test_route_installed_when_live_next_hop_is_a_different_address(self):
        # The normalised comparison must not over-match: a genuinely
        # different next hop does not establish reachability via the
        # gateway, so the temporary route is still required.
        device = make_device(gateway={'ipv6': ['2001:0db8:1:0::1']},
                             next_hops=['2001:db8:1::2'])
        temporary_route = self._add(
            device, destination='scp://[2001:db8::10]//tmp/a.bin')
        self.assertEqual(temporary_route['prefix'], '2001:db8::10/128')
        device.api.configure_static_routing_route.assert_called_once_with(
            prefix='2001:db8::10/128', next_hop='2001:0db8:1:0::1',
            address_family='ipv6', vrf='Mgmt-vrf')

    def test_route_installed_when_live_next_hop_list_is_empty(self):
        # An empty next-hop list must not be treated as a match.
        device = make_device(gateway={'ipv4': '192.0.2.1'}, next_hops=[])
        temporary_route = self._add(device)
        self.assertEqual(temporary_route['prefix'], '1.2.3.4/32')
        device.api.configure_static_routing_route.assert_called_once_with(
            prefix='1.2.3.4/32', next_hop='192.0.2.1',
            address_family='ipv4', vrf='Mgmt-vrf')

    def test_route_installed_when_live_next_hop_is_not_an_address(self):
        # Non-parsing values fall back to a string comparison, so an
        # interface-style next hop does not spuriously match the gateway.
        device = make_device(gateway={'ipv4': '192.0.2.1'},
                             next_hops=['GigabitEthernet0/0/0/0'])
        temporary_route = self._add(device)
        self.assertEqual(temporary_route['prefix'], '1.2.3.4/32')
        device.api.configure_static_routing_route.assert_called_once_with(
            prefix='1.2.3.4/32', next_hop='192.0.2.1',
            address_family='ipv4', vrf='Mgmt-vrf')

    def test_ipv4_route_installed(self):
        device = make_device(gateway={'ipv4': '192.0.2.1'})
        temporary_route = self._add(device)
        self.assertEqual(
            temporary_route,
            {'prefix': '1.2.3.4/32', 'next_hop': '192.0.2.1',
             'address_family': 'ipv4', 'vrf': 'Mgmt-vrf'})
        device.api.configure_static_routing_route.assert_called_once_with(
            prefix='1.2.3.4/32', next_hop='192.0.2.1',
            address_family='ipv4', vrf='Mgmt-vrf')

    def test_ipv6_route_installed(self):
        device = make_device(gateway={'ipv6': '2001:db8:1::1'})
        temporary_route = self._add(
            device, destination='scp://[2001:db8::10]//tmp/a.bin')
        self.assertEqual(temporary_route['prefix'], '2001:db8::10/128')
        device.api.configure_static_routing_route.assert_called_once_with(
            prefix='2001:db8::10/128', next_hop='2001:db8:1::1',
            address_family='ipv6', vrf='Mgmt-vrf')

    def test_route_lookup_failure_skips_install(self):
        # A lookup that does not complete leaves reachability unknown; the
        # routing table must be left untouched rather than guessed at.
        device = make_device(gateway={'ipv4': '192.0.2.1'})
        device.api.get_routing_route_next_hop.side_effect = Exception('boom')
        self.assertIsNone(self._add(device))
        device.api.configure_static_routing_route.assert_not_called()

    def test_declared_management_route_via_gateway_skips_install(self):
        # pyATS device-management schema spelling: 'next-hop'. The declared
        # next hop is the gateway, so reachability via the gateway is
        # already asserted by the testbed.
        device = make_device(
            gateway={'ipv4': '192.0.2.1'},
            routes={'ipv4': [{'subnet': '1.2.0.0/16',
                              'next-hop': '192.0.2.1'}]})
        self.assertIsNone(self._add(device))
        device.api.configure_static_routing_route.assert_not_called()

    def test_declared_management_route_normalized_key(self):
        # Normalised testbeds expose the same leaf as 'next_hop'.
        device = make_device(
            gateway={'ipv4': '192.0.2.1'},
            routes={'ipv4': [{'subnet': '1.2.3.4/32',
                              'next_hop': '192.0.2.1'}]})
        self.assertIsNone(self._add(device))
        device.api.configure_static_routing_route.assert_not_called()

    def test_declared_route_next_hop_prefix_is_stripped(self):
        device = make_device(
            gateway={'ipv4': '192.0.2.1'},
            routes={'ipv4': [{'subnet': '1.2.0.0/16',
                              'next-hop': '192.0.2.1/24'}]})
        self.assertIsNone(self._add(device))
        device.api.configure_static_routing_route.assert_not_called()

    def test_declared_route_via_other_next_hop_still_installs(self):
        # The route covers the endpoint but points somewhere other than the
        # management gateway, so it says nothing about reachability via that
        # gateway and must not suppress the temporary route.
        device = make_device(
            gateway={'ipv4': '192.0.2.1'},
            routes={'ipv4': [{'subnet': '1.2.0.0/16',
                              'next-hop': '192.0.2.9'}]})
        self.assertIsNotNone(self._add(device))
        device.api.configure_static_routing_route.assert_called_once_with(
            prefix='1.2.3.4/32', next_hop='192.0.2.1',
            address_family='ipv4', vrf='Mgmt-vrf')

    def test_declared_ipv6_management_route_skips_install(self):
        # Written in a different but equivalent IPv6 form to the gateway.
        device = make_device(
            gateway={'ipv6': '2001:db8:1::1'},
            routes={'ipv6': [{'subnet': '2001:db8::/32',
                              'next-hop': '2001:0db8:1:0::1'}]})
        self.assertIsNone(
            self._add(device, destination='scp://[2001:db8::10]//tmp/a.bin'))
        device.api.configure_static_routing_route.assert_not_called()

    def test_declared_ipv6_route_via_other_next_hop_still_installs(self):
        device = make_device(
            gateway={'ipv6': '2001:db8:1::1'},
            routes={'ipv6': [{'subnet': '2001:db8::/32',
                              'next-hop': '2001:db8:1::9'}]})
        self.assertIsNotNone(
            self._add(device, destination='scp://[2001:db8::10]//tmp/a.bin'))
        device.api.configure_static_routing_route.assert_called_once_with(
            prefix='2001:db8::10/128', next_hop='2001:db8:1::1',
            address_family='ipv6', vrf='Mgmt-vrf')

    def test_declared_route_not_covering_endpoint_still_installs(self):
        device = make_device(
            gateway={'ipv4': '192.0.2.1'},
            routes={'ipv4': [{'subnet': '10.0.0.0/8',
                              'next-hop': '192.0.2.1'}]})
        self.assertIsNotNone(self._add(device))
        device.api.configure_static_routing_route.assert_called_once_with(
            prefix='1.2.3.4/32', next_hop='192.0.2.1',
            address_family='ipv4', vrf='Mgmt-vrf')

    def test_longest_prefix_wins_when_specific_route_listed_last(self):
        # A broad route via the gateway is listed first, but a more
        # specific one points elsewhere. The device would follow the
        # longer prefix, so the endpoint is not reachable via the gateway
        # and the temporary route must still be installed.
        device = make_device(
            gateway={'ipv4': '192.0.2.1'},
            routes={'ipv4': [{'subnet': '0.0.0.0/0',
                              'next-hop': '192.0.2.1'},
                             {'subnet': '1.2.3.0/24',
                              'next-hop': '192.0.2.9'}]})
        self.assertIsNotNone(self._add(device))
        device.api.configure_static_routing_route.assert_called_once_with(
            prefix='1.2.3.4/32', next_hop='192.0.2.1',
            address_family='ipv4', vrf='Mgmt-vrf')

    def test_longest_prefix_wins_when_specific_route_listed_first(self):
        # Mirror image: the specific route via the gateway is listed
        # before a broad route pointing elsewhere. The longest prefix
        # names the gateway, so nothing needs configuring.
        device = make_device(
            gateway={'ipv4': '192.0.2.1'},
            routes={'ipv4': [{'subnet': '1.2.3.0/24',
                              'next-hop': '192.0.2.1'},
                             {'subnet': '0.0.0.0/0',
                              'next-hop': '192.0.2.9'}]})
        self.assertIsNone(self._add(device))
        device.api.configure_static_routing_route.assert_not_called()

    def test_longest_prefix_selected_among_several_covering_routes(self):
        device = make_device(
            gateway={'ipv4': '192.0.2.1'},
            routes={'ipv4': [{'subnet': '1.2.3.4/32',
                              'next-hop': '192.0.2.1'},
                             {'subnet': '0.0.0.0/0',
                              'next-hop': '192.0.2.8'},
                             {'subnet': '1.2.0.0/16',
                              'next-hop': '192.0.2.9'}]})
        self.assertEqual(
            self.fu._get_declared_route_next_hop(device, '1.2.3.4', 'ipv4'),
            '192.0.2.1')

    def test_equal_prefix_length_keeps_first_declared_route(self):
        device = make_device(
            gateway={'ipv4': '192.0.2.1'},
            routes={'ipv4': [{'subnet': '1.2.3.0/24',
                              'next-hop': '192.0.2.1'},
                             {'subnet': '1.2.3.0/24',
                              'next-hop': '192.0.2.9'}]})
        self.assertEqual(
            self.fu._get_declared_route_next_hop(device, '1.2.3.4', 'ipv4'),
            '192.0.2.1')

    def test_longest_prefix_wins_for_ipv6(self):
        device = make_device(
            gateway={'ipv6': '2001:db8:1::1'},
            routes={'ipv6': [{'subnet': '::/0',
                              'next-hop': '2001:db8:1::1'},
                             {'subnet': '2001:db8::/32',
                              'next-hop': '2001:db8:1::9'}]})
        self.assertIsNotNone(
            self._add(device, destination='scp://[2001:db8::10]//tmp/a.bin'))
        device.api.configure_static_routing_route.assert_called_once_with(
            prefix='2001:db8::10/128', next_hop='2001:db8:1::1',
            address_family='ipv6', vrf='Mgmt-vrf')

    def test_malformed_route_does_not_mask_longer_prefix(self):
        # A malformed entry is skipped without aborting the scan, so a
        # more specific route declared after it is still selected.
        device = make_device(
            gateway={'ipv4': '192.0.2.1'},
            routes={'ipv4': [{'subnet': '0.0.0.0/0',
                              'next-hop': '192.0.2.1'},
                             {'subnet': 'not-a-subnet',
                              'next-hop': '192.0.2.8'},
                             {'subnet': '1.2.3.0/24',
                              'next-hop': '192.0.2.9'}]})
        self.assertEqual(
            self.fu._get_declared_route_next_hop(device, '1.2.3.4', 'ipv4'),
            '192.0.2.9')

    def test_declared_route_of_other_family_is_ignored(self):
        device = make_device(
            gateway={'ipv4': '192.0.2.1'},
            routes={'ipv6': [{'subnet': '::/0', 'next-hop': '2001:db8::1'}]})
        self.assertIsNotNone(self._add(device))
        device.api.configure_static_routing_route.assert_called_once()

    def test_malformed_declared_route_is_ignored(self):
        device = make_device(
            gateway={'ipv4': '192.0.2.1'},
            routes={'ipv4': [{'subnet': 'not-a-subnet',
                              'next-hop': '192.0.2.1'},
                             {'subnet': '1.2.3.0/24'}]})
        self.assertIsNotNone(self._add(device))
        device.api.configure_static_routing_route.assert_called_once()

    def test_install_failure_is_not_fatal(self):
        device = make_device(gateway={'ipv4': '192.0.2.1'})
        device.api.configure_static_routing_route.side_effect = \
            Exception('boom')
        self.assertIsNone(self._add(device))

    def test_partial_configuration_failure_rolls_back_route(self):
        # The route may already be applied when the configuration call
        # raises (e.g. a later line of the session is rejected). Nothing
        # is returned, so the caller holds no cleanup record; the failure
        # path must therefore remove the route itself or it outlives the
        # transfer.
        device = make_device(gateway={'ipv4': '192.0.2.1'})
        device.api.configure_static_routing_route.side_effect = \
            Exception('route applied, later config line rejected')

        self.assertIsNone(self._add(device))

        device.api.unconfigure_static_routing_route.\
            assert_called_once_with(prefix='1.2.3.4/32',
                                    next_hop='192.0.2.1',
                                    address_family='ipv4',
                                    vrf='Mgmt-vrf')

    def test_rollback_failure_is_not_fatal(self):
        # Both the configuration and the rollback fail: the transfer must
        # still proceed rather than propagating either exception.
        device = make_device(gateway={'ipv4': '192.0.2.1'})
        device.api.configure_static_routing_route.side_effect = \
            Exception('boom')
        device.api.unconfigure_static_routing_route.side_effect = \
            Exception('rollback boom')

        self.assertIsNone(self._add(device))
        device.api.unconfigure_static_routing_route.assert_called_once()

    def test_successful_install_does_not_roll_back(self):
        device = make_device(gateway={'ipv4': '192.0.2.1'})
        self.assertIsNotNone(self._add(device))
        device.api.unconfigure_static_routing_route.assert_not_called()


class TestRemoveTemporaryTransferRoute(unittest.TestCase):

    def setUp(self):
        self.fu = make_fileutils()
        self.temporary_route = {'prefix': '1.2.3.4/32',
                                'next_hop': '192.0.2.1',
                                'address_family': 'ipv4',
                                'vrf': 'Mgmt-vrf'}

    def test_removes_exact_route(self):
        device = make_device()
        self.fu._remove_temporary_transfer_route(device, self.temporary_route)
        device.api.unconfigure_static_routing_route.assert_called_once_with(
            prefix='1.2.3.4/32', next_hop='192.0.2.1',
            address_family='ipv4', vrf='Mgmt-vrf')

    def test_noop_when_nothing_was_added(self):
        device = make_device()
        self.fu._remove_temporary_transfer_route(device, None)
        device.api.unconfigure_static_routing_route.assert_not_called()

    def test_removes_default_vrf_route(self):
        device = make_device()
        self.fu._remove_temporary_transfer_route(
            device, dict(self.temporary_route, vrf=None))
        device.api.unconfigure_static_routing_route.assert_called_once_with(
            prefix='1.2.3.4/32', next_hop='192.0.2.1',
            address_family='ipv4', vrf=None)

    def test_removal_failure_is_swallowed(self):
        device = make_device()
        device.api.unconfigure_static_routing_route.side_effect = \
            Exception('boom')
        self.assertIsNone(self.fu._remove_temporary_transfer_route(
            device, self.temporary_route))


class TestFileTransferConfigLifecycle(unittest.TestCase):
    """The temporary route must be cleaned up on success and on failure."""

    def setUp(self):
        self.fu = make_fileutils()
        self.device = make_device(gateway={'ipv4': '192.0.2.1'})
        self.kwargs = dict(device=self.device,
                           source='flash:/a.bin',
                           destination='scp://1.2.3.4//tmp/a.bin',
                           vrf='Mgmt-vrf',
                           jit_route=True,
                           wait_after_restore=0)

    def _expected_removal(self):
        return call(prefix='1.2.3.4/32', next_hop='192.0.2.1',
                    address_family='ipv4', vrf='Mgmt-vrf')

    def test_cleanup_on_success(self):
        with self.fu.file_transfer_config(**self.kwargs):
            pass
        self.assertIn(self._expected_removal(),
                      self.device.api.unconfigure_static_routing_route
                      .call_args_list)

    def test_cleanup_on_transfer_exception(self):
        with self.assertRaises(RuntimeError):
            with self.fu.file_transfer_config(**self.kwargs):
                raise RuntimeError('transfer failed')
        self.assertIn(self._expected_removal(),
                      self.device.api.unconfigure_static_routing_route
                      .call_args_list)

    def test_cleanup_exception_does_not_mask_transfer_error(self):
        self.device.api.unconfigure_static_routing_route.side_effect = \
            Exception('cleanup failed')
        with self.assertRaises(RuntimeError):
            with self.fu.file_transfer_config(**self.kwargs):
                raise RuntimeError('transfer failed')

    def test_route_still_configured_when_flag_is_off(self):
        # The legacy ``jit_route`` opt-in flag is inert: temporary transfer
        # routing is the default behaviour on IOSXR.
        self.kwargs['jit_route'] = False
        with self.fu.file_transfer_config(**self.kwargs):
            pass
        self.device.api.configure_static_routing_route.assert_called_once_with(
            prefix='1.2.3.4/32', next_hop='192.0.2.1',
            address_family='ipv4', vrf='Mgmt-vrf')
        self.assertIn(self._expected_removal(),
                      self.device.api.unconfigure_static_routing_route
                      .call_args_list)


class TestHttpsFileTransferConfigLifecycle(unittest.TestCase):
    """The HTTPS setup path must not strand the temporary route.

    ``HTTPFileUtilsBase.file_transfer_config`` sets the clock, fetches the
    server certificate and configures a DNS host entry and trustpoint after
    the temporary route is installed. All of that has to sit inside the
    protected block: otherwise an exception raised there escapes before the
    ``finally`` is ever armed and strands the static route on the device.
    """

    def setUp(self):
        self.fu = make_https_fileutils()
        self.fu.url_mapping = {}
        self.device = make_device(gateway={'ipv4': '192.0.2.1'})
        self.kwargs = dict(device=self.device,
                           source='flash:/a.bin',
                           destination='scp://1.2.3.4//tmp/a.bin',
                           vrf='Mgmt-vrf',
                           wait_after_restore=0)

    def _expected_removal(self):
        return call(prefix='1.2.3.4/32', next_hop='192.0.2.1',
                    address_family='ipv4', vrf='Mgmt-vrf')

    def test_cleanup_on_setup_failure(self):
        # The clock set is the first setup step after the route install.
        self.device.execute.side_effect = Exception('clock set failed')

        with self.assertRaises(Exception) as raised:
            with self.fu.file_transfer_config(**self.kwargs):
                self.fail('body must not run when setup fails')

        self.assertIn('clock set failed', str(raised.exception))
        # The route was configured, then removed despite the failure.
        self.device.api.configure_static_routing_route.assert_called_once_with(
            prefix='1.2.3.4/32', next_hop='192.0.2.1',
            address_family='ipv4', vrf='Mgmt-vrf')
        self.assertIn(self._expected_removal(),
                      self.device.api.unconfigure_static_routing_route
                      .call_args_list)

    def test_cleanup_on_success(self):
        with self.fu.file_transfer_config(**self.kwargs):
            pass
        self.assertIn(self._expected_removal(),
                      self.device.api.unconfigure_static_routing_route
                      .call_args_list)


class TestGetRoutingRouteNextHop(unittest.TestCase):
    """Regression tests for the IOSXR next-hop extraction.

    ``Dq.get_values('next_hop')`` cannot be used here: the IOSXR schema
    names both the outer container and the leaf ``next_hop``, so the query
    matches the container first and flattens it to its keys, returning the
    literal string ``'next_hop_list'`` instead of an address.
    """

    @staticmethod
    def _device(parsed):
        device = MagicMock()
        device.name = 'xr1'
        # Real parser output exposes a ``.q`` Dq accessor; plain dicts do not.
        device.parse.return_value = _QDict(parsed)
        return device

    # Shape produced by 'show route ipv4 5.1.21.11' on a real IOSXR box,
    # where the hit is the covering route 5.0.0.0/8 via the mgmt gateway.
    COVERING_ROUTE = {
        'vrf': {
            'default': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '5.0.0.0/8': {
                                'route': '5.0.0.0/8',
                                'known_via': 'static',
                                'source_protocol': 'static',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '5.2.0.1',
                                            'outgoing_interface':
                                                'MgmtEth0/RP0/CPU0/0',
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    CONNECTED_ROUTE = {
        'vrf': {
            'default': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '5.2.0.0/16': {
                                'route': '5.2.0.0/16',
                                'known_via': 'connected',
                                'source_protocol': 'connected',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'MgmtEth0/RP0/CPU0/0': {
                                            'outgoing_interface':
                                                'MgmtEth0/RP0/CPU0/0',
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    def test_next_hop_list_yields_addresses_not_container_keys(self):
        device = self._device(self.COVERING_ROUTE)
        result = get_routing_route_next_hop(
            device, '5.1.21.11', address_family='ipv4')
        self.assertEqual(result['next_hops'], ['5.2.0.1'])
        self.assertNotIn('next_hop_list', result['next_hops'])
        self.assertEqual(result['route'], '5.0.0.0/8')
        self.assertEqual(result['outgoing_interfaces'],
                         ['MgmtEth0/RP0/CPU0/0'])
        self.assertFalse(result['connected'])

    def test_gateway_guard_matches_covering_route(self):
        device = self._device(self.COVERING_ROUTE)
        result = get_routing_route_next_hop(
            device, '5.1.21.11', address_family='ipv4')
        self.assertIn('5.2.0.1', result['next_hops'])

    def test_connected_route_has_no_next_hops(self):
        device = self._device(self.CONNECTED_ROUTE)
        result = get_routing_route_next_hop(
            device, '5.2.24.22', address_family='ipv4')
        self.assertEqual(result['next_hops'], [])
        self.assertEqual(result['outgoing_interfaces'],
                         ['MgmtEth0/RP0/CPU0/0'])
        self.assertTrue(result['connected'])

    def test_empty_parsed_output_returns_none(self):
        self.assertIsNone(get_routing_route_next_hop(
            self._device({}), '5.1.21.11', address_family='ipv4'))

    def test_schema_empty_parser_error_returns_none(self):
        # The device answered, it simply has no route for the address.
        device = MagicMock()
        device.name = 'xr1'
        device.parse.side_effect = SchemaEmptyParserError('no data')
        self.assertIsNone(get_routing_route_next_hop(
            device, '5.1.21.11', address_family='ipv4'))

    def test_unexpected_parse_failure_propagates(self):
        # Reachability is unknown, so this must not look like 'no route'.
        device = MagicMock()
        device.name = 'xr1'
        device.parse.side_effect = ConnectionError('boom')
        with self.assertRaises(ConnectionError):
            get_routing_route_next_hop(device, '5.1.21.11',
                                       address_family='ipv4')

    def test_invalid_route_raises(self):
        device = self._device(self.COVERING_ROUTE)
        with self.assertRaises(ValueError):
            get_routing_route_next_hop(device, 'not-an-address')

    def test_vrf_is_included_in_command(self):
        device = self._device(self.COVERING_ROUTE)
        get_routing_route_next_hop(device, '5.1.21.11',
                                   address_family='ipv4', vrf='Mgmt-vrf')
        device.parse.assert_called_once_with(
            'show route vrf Mgmt-vrf ipv4 5.1.21.11')


if __name__ == '__main__':
    unittest.main()
