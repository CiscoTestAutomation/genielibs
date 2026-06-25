import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authentication
from unicon.core.errors import SubCommandFailure


class TestConfigureAaaAuthentication(unittest.TestCase):

    def test_configure_login_single_group(self):
        device = Mock()
        configure_aaa_authentication(device, 'login', 'AUTHEN_LIST', ['group RADIUS_GRP'])
        device.configure.assert_called_once_with(
            'aaa authentication login AUTHEN_LIST group RADIUS_GRP'
        )

    def test_configure_login_default_group(self):
        device = Mock()
        configure_aaa_authentication(device, 'login', 'default', ['group RADIUS_GRP'])
        device.configure.assert_called_once_with(
            'aaa authentication login default group RADIUS_GRP'
        )

    def test_configure_login_group_with_local_fallback(self):
        device = Mock()
        configure_aaa_authentication(device, 'login', 'default', ['group RADIUS_GRP', 'local'])
        device.configure.assert_called_once_with(
            'aaa authentication login default group RADIUS_GRP local'
        )

    def test_configure_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_aaa_authentication(device, 'login', 'AUTHEN_LIST', ['group RADIUS_GRP'])


if __name__ == '__main__':
    unittest.main()
