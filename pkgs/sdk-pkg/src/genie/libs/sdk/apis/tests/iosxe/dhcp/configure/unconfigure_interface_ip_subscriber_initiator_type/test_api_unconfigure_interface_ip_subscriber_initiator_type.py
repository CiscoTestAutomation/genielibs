from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_interface_ip_subscriber_initiator_type
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure


class TestUnconfigureInterfaceIpSubscriberInitiatorType(TestCase):

    def test_unconfigure_interface_ip_subscriber_initiator_dhcp(self):
        self.device = Mock()
        unconfigure_interface_ip_subscriber_initiator_type(
            self.device, 'GigabitEthernet0/0/1', 'l2-connected', 'dhcp'
        )
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ([
                'interface GigabitEthernet0/0/1',
                'ip subscriber l2-connected',
                'no initiator dhcp',
            ],)
        )

    def test_unconfigure_interface_ip_subscriber_initiator_radius_proxy(self):
        self.device = Mock()
        unconfigure_interface_ip_subscriber_initiator_type(
            self.device, 'GigabitEthernet0/0/1', 'l2-connected', 'radius-proxy'
        )
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ([
                'interface GigabitEthernet0/0/1',
                'ip subscriber l2-connected',
                'no initiator radius-proxy',
            ],)
        )

    def test_unconfigure_interface_ip_subscriber_initiator_type_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('bad config')
        with self.assertRaises(SubCommandFailure):
            unconfigure_interface_ip_subscriber_initiator_type(
                self.device, 'GigabitEthernet0/0/1', 'l2-connected', 'dhcp'
            )
