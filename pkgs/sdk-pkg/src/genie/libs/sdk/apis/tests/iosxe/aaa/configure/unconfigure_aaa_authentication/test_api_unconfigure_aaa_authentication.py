import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_authentication
from unicon.core.errors import SubCommandFailure


class TestUnconfigureAaaAuthentication(unittest.TestCase):

    def test_unconfigure_login(self):
        device = Mock()
        unconfigure_aaa_authentication(device, 'login', 'AUTHEN_LIST', ['group RADIUS_GRP'])
        device.configure.assert_called_once_with(
            'no aaa authentication login AUTHEN_LIST group RADIUS_GRP'
        )

    def test_unconfigure_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_aaa_authentication(device, 'login', 'AUTHEN_LIST', ['group RADIUS_GRP'])


if __name__ == '__main__':
    unittest.main()
