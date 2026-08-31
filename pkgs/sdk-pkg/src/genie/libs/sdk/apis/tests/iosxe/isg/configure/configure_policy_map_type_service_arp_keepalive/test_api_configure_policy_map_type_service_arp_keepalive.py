from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.isg.configure import (
    configure_policy_map_type_service_arp_keepalive,
)


class TestConfigurePolicyMapTypeServiceArpKeepalive(TestCase):

    def test_configure_policy_map_type_service_arp_keepalive(self):
        device = Mock()
        configure_policy_map_type_service_arp_keepalive(device)

        device.configure.assert_called_once_with([
            "policy-map type service ARP_KEEPALIVE",
            " keepalive idle 35 attempts 10 interval 20 protocol ARP",
        ])

    def test_configure_policy_map_type_service_arp_keepalive_custom(self):
        device = Mock()
        configure_policy_map_type_service_arp_keepalive(
            device,
            policy_map_name='KEEPALIVE_CUSTOM',
            idle=10,
            attempts=2,
            interval=5,
            protocol='ARP',
        )

        device.configure.assert_called_once_with([
            "policy-map type service KEEPALIVE_CUSTOM",
            " keepalive idle 10 attempts 2 interval 5 protocol ARP",
        ])

    def test_configure_policy_map_type_service_arp_keepalive_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_policy_map_type_service_arp_keepalive(device)
