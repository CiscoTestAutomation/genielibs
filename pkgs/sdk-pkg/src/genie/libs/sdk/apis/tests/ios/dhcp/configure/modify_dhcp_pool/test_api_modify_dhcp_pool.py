from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog

from genie.libs.sdk.apis.ios.dhcp.configure import modify_dhcp_pool


class TestModifyDhcpPool(TestCase):

    def _assert_config_with_reply(self, expected_config):
        self.device.configure.assert_called_once()
        args, kwargs = self.device.configure.call_args
        self.assertEqual(args[0], expected_config)
        self.assertIn('reply', kwargs)
        self.assertIsInstance(kwargs['reply'], Dialog)

    def test_modify_dhcp_pool_add(self):
        self.device = Mock()
        modify_dhcp_pool(
            self.device,
            pool_name='DS_POOL',
            network='11.11.11.0',
            mask='255.255.255.0',
            router_id='11.11.11.1',
            lease_days='0', lease_hrs='1', lease_mins='0',
        )
        self._assert_config_with_reply(
            [
                "ip dhcp pool DS_POOL",
                "network 11.11.11.0 255.255.255.0",
                "default-router 11.11.11.1",
                "lease 0 1 0",
            ]
        )

    def test_modify_dhcp_pool_remove(self):
        self.device = Mock()
        modify_dhcp_pool(
            self.device,
            pool_name='DS_POOL',
            router_id='11.11.11.1',
            network='11.11.11.0',
            mask='255.255.255.0',
            vrf='RED',
            dns_server='8.8.8.8',
            negate=True,
        )
        self._assert_config_with_reply(
            [
                "ip dhcp pool DS_POOL",
                "no vrf RED",
                "no network 11.11.11.0 255.255.255.0",
                "no default-router 11.11.11.1",
                "no dns-server 8.8.8.8",
            ]
        )

    def test_modify_dhcp_pool_update_network_and_vrf(self):
        self.device = Mock()
        modify_dhcp_pool(
            self.device,
            pool_name='DS_POOL',
            network='11.11.11.0',
            mask='255.255.255.0',
            vrf='RED',
        )
        self._assert_config_with_reply(
            [
                "ip dhcp pool DS_POOL",
                "vrf RED",
                "network 11.11.11.0 255.255.255.0",
            ]
        )

    def test_modify_dhcp_pool_multi_address(self):
        self.device = Mock()
        modify_dhcp_pool(
            self.device,
            pool_name='DS_POOL',
            router_id=['11.11.11.1', '11.11.11.2'],
            dns_server=('8.8.8.8', '8.8.4.4'),
        )
        self._assert_config_with_reply(
            [
                "ip dhcp pool DS_POOL",
                "default-router 11.11.11.1 11.11.11.2",
                "dns-server 8.8.8.8 8.8.4.4",
            ]
        )

    def test_modify_dhcp_pool_lease_infinite_remove(self):
        self.device = Mock()
        modify_dhcp_pool(
            self.device,
            pool_name='DS_POOL',
            domain_name='cisco.com',
            lease_infinite=True,
            negate=True,
        )
        self._assert_config_with_reply(
            [
                "ip dhcp pool DS_POOL",
                "no domain-name cisco.com",
                "no lease infinite",
            ]
        )

    def test_modify_dhcp_pool_no_subcommands_noop(self):
        self.device = Mock()
        modify_dhcp_pool(self.device, pool_name='DS_POOL')
        self.device.configure.assert_not_called()

    def test_modify_dhcp_pool_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            modify_dhcp_pool(
                self.device, pool_name='DS_POOL', vrf='RED',
            )
