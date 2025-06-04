from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_interface
from unittest.mock import Mock


class TestConfigureRadiusInterface(TestCase):

    def test_configure_radius_interface(self):
        self.device = Mock()
        configure_radius_interface(self.device, 'Loopback0', 'ipv4')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip radius source-interface Loopback0'],)
        )

