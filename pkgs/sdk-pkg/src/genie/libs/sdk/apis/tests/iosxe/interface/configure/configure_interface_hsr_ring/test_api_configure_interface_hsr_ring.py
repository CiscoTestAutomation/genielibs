from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_hsr_ring
from unittest.mock import Mock


class TestConfigureInterfaceHsrRing(TestCase):

    def test_configure_interface_hsr_ring(self):
        self.device = Mock()
        result = configure_interface_hsr_ring(self.device, 'Gi1/1', 1)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Gi1/1', 'hsr-ring 1'],)
        )
