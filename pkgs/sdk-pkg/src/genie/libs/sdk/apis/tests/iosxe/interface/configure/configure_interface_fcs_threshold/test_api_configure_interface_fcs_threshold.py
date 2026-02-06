from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_fcs_threshold
from unittest.mock import Mock


class TestConfigureInterfaceFcsThreshold(TestCase):

    def test_configure_interface_fcs_threshold(self):
        self.device = Mock()
        result = configure_interface_fcs_threshold(self.device, 'Gi1/0/2', 10)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Gi1/0/2', 'fcs-threshold 10'],)
        )
