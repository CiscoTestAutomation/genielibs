from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_interface_ip_subscriber_initiator


class TestUnconfigureInterfaceIpSubscriberInitiator(TestCase):

    def test_unconfigure_with_option_and_type(self):
        self.device = Mock()
        unconfigure_interface_ip_subscriber_initiator(
            self.device, 'GigabitEthernet0/0', 'l2-connected',
            option='mac-address', type='ipv6'
        )
        self.device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                " ip subscriber l2-connected",
                "  no initiator unclassified mac-address ipv6",
            ]
        )

    def test_unconfigure_with_option_only(self):
        self.device = Mock()
        unconfigure_interface_ip_subscriber_initiator(
            self.device, 'GigabitEthernet0/0', 'l2-connected',
            option='mac-address'
        )
        self.device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                " ip subscriber l2-connected",
                "  no initiator unclassified mac-address",
            ]
        )

    def test_unconfigure_bare(self):
        self.device = Mock()
        unconfigure_interface_ip_subscriber_initiator(
            self.device, 'GigabitEthernet0/0', 'l2-connected'
        )
        self.device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                " ip subscriber l2-connected",
                "  no initiator unclassified",
            ]
        )

    def test_unconfigure_with_remove_subscriber(self):
        self.device = Mock()
        unconfigure_interface_ip_subscriber_initiator(
            self.device, 'GigabitEthernet0/0', 'l2-connected',
            option='mac-address', type='ipv6', remove_subscriber=True
        )
        self.device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                " ip subscriber l2-connected",
                "  no initiator unclassified mac-address ipv6",
                " no ip subscriber l2-connected",
            ]
        )

    def test_unconfigure_type_without_option_raises(self):
        self.device = Mock()
        with self.assertRaises(ValueError):
            unconfigure_interface_ip_subscriber_initiator(
                self.device, 'GigabitEthernet0/0', 'l2-connected',
                type='ipv6'
            )

    def test_unconfigure_device_configure_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_interface_ip_subscriber_initiator(
                self.device, 'GigabitEthernet0/0', 'l2-connected',
                option='mac-address'
            )
