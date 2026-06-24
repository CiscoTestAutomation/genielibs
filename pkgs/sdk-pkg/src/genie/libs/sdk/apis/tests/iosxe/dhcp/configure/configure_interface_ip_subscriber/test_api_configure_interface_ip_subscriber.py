from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_interface_ip_subscriber
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure


class TestConfigureInterfaceIpSubscriber(TestCase):

    def test_configure_interface_ip_subscriber(self):
        self.device = Mock()
        result = configure_interface_ip_subscriber(self.device, 'GigabitEthernet0/0/1', 'l2-connected', None, None, None, None, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/0/1', 'ip subscriber l2-connected'],)
        )

    def test_configure_interface_ip_subscriber_initiator_dhcp(self):
        # Backward-compat: existing keyword usage from ISG dual-stack tests
        self.device = Mock()
        configure_interface_ip_subscriber(
            self.device, 'GigabitEthernet0/0/1', ip_session='l2-connected',
            type='dhcp', initiator=True,
        )
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ([
                'interface GigabitEthernet0/0/1',
                'ip subscriber l2-connected',
                'initiator dhcp',
            ],)
        )

    def test_configure_interface_ip_subscriber_initiator_unclassified(self):
        # Backward-compat: 'initiator unclassified mac-address' branch
        self.device = Mock()
        configure_interface_ip_subscriber(
            self.device, 'GigabitEthernet0/0/1', ip_session='l2-connected',
            option='mac-address', initiator=True, value='mac-address',
        )
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ([
                'interface GigabitEthernet0/0/1',
                'ip subscriber l2-connected',
                'initiator unclassified mac-address',
            ],)
        )

    def test_configure_interface_ip_subscriber_failure(self):
        # Failure path: SubCommandFailure propagated
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('bad config')
        with self.assertRaises(SubCommandFailure):
            configure_interface_ip_subscriber(
                self.device, 'GigabitEthernet0/0/1', ip_session='l2-connected',
                type='dhcp', initiator=True,
            )
