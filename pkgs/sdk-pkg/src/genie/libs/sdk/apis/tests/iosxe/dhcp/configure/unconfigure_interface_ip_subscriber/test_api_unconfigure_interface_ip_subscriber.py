from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_interface_ip_subscriber
from unittest.mock import Mock


class TestUnconfigureInterfaceIpSubscriber(TestCase):

    def test_unconfigure_interface_ip_subscriber(self):
        self.device = Mock()
        result = unconfigure_interface_ip_subscriber(self.device, 'GigabitEthernet0/0/1', 'l2-connected')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/0/1', 'no ip subscriber l2-connected'],)
        )
