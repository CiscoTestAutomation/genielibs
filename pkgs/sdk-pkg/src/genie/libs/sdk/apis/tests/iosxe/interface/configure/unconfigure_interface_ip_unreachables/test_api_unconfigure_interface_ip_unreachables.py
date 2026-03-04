from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_ip_unreachables
from unittest.mock import Mock


class TestUnconfigureInterfaceIpUnreachables(TestCase):

    def test_unconfigure_interface_ip_unreachables(self):
        self.device = Mock()
        result = unconfigure_interface_ip_unreachables(self.device, 'Port-channel1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Port-channel1', 'no ip unreachables'],)
        )
