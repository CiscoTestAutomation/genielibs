from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.radius.configure import configure_radius_server_key


class TestConfigureRadiusServerKey(TestCase):

    def test_configure_radius_server_key(self):
        self.device = Mock()
        configure_radius_server_key(self.device, 'cisco123')
        self.device.configure.assert_called_once_with(
            "radius-server key cisco123"
        )

    def test_configure_radius_server_key_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_radius_server_key(self.device, 'cisco123')
