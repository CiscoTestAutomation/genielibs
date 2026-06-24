from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.ios.dhcp.configure import create_dhcp_pool


class TestCreateDhcpPool(TestCase):

    def test_create_dhcp_pool(self):
        self.device = Mock()
        create_dhcp_pool(
            self.device,
            pool_name='DS_POOL',
            network='11.11.11.0',
            mask='255.255.255.0',
            router_id='11.11.11.1',
            lease_days='0',
            lease_hrs='1',
            lease_mins='0',
        )
        self.device.configure.assert_called_once_with(
            [
                "ip dhcp pool DS_POOL",
                "network 11.11.11.0 255.255.255.0",
                "default-router 11.11.11.1",
                "lease 0 1 0",
            ]
        )

    def test_create_dhcp_pool_positional(self):
        self.device = Mock()
        create_dhcp_pool(
            self.device, 'POOL1', '10.0.0.0', '255.255.255.0',
            '10.0.0.1', '7', '0', '0',
        )
        self.device.configure.assert_called_once_with(
            [
                "ip dhcp pool POOL1",
                "network 10.0.0.0 255.255.255.0",
                "default-router 10.0.0.1",
                "lease 7 0 0",
            ]
        )

    def test_create_dhcp_pool_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            create_dhcp_pool(
                self.device, 'POOL1', '10.0.0.0', '255.255.255.0',
                '10.0.0.1', '0', '1', '0',
            )
