from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.radius.configure import unconfigure_radius_server_key


class TestUnconfigureRadiusServerKey(TestCase):

    def test_unconfigure_radius_server_key(self):
        self.device = Mock()
        unconfigure_radius_server_key(self.device, 'cisco123')
        self.device.configure.assert_called_once_with(
            "no radius-server key cisco123"
        )

    def test_unconfigure_radius_server_key_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_radius_server_key(self.device, 'cisco123')
