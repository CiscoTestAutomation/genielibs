from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_hsr_ring
from unittest.mock import Mock


class TestUnconfigureInterfaceHsrRing(TestCase):

    def test_unconfigure_interface_hsr_ring(self):
        self.device = Mock()
        result = unconfigure_interface_hsr_ring(self.device, 1)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no interface hsr-ring 1'],)
        )
