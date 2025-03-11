from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_interface_ip_subscriber
from unittest.mock import Mock


class TestConfigureInterfaceIpSubscriber(TestCase):

    def test_configure_interface_ip_subscriber(self):
        self.device = Mock()
        result = configure_interface_ip_subscriber(self.device, 'GigabitEthernet0/0/1', 'l2-connected', None, None, None, None, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/0/1', 'ip subscriber l2-connected'],)
        )
