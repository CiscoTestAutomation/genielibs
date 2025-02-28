from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_ip_unnumbered_on_interface
from unittest.mock import Mock


class TestUnconfigureIpUnnumberedOnInterface(TestCase):

    def test_unconfigure_ip_unnumbered_on_interface(self):
        self.device = Mock()
        result = unconfigure_ip_unnumbered_on_interface(self.device, 'GigabitEthernet1/0/8', 'GigabitEthernet1/0/7', False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/8', 'no ip unnumbered GigabitEthernet1/0/7'],)
        )
