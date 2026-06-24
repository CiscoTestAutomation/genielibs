import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_authorization
from unicon.core.errors import SubCommandFailure


class TestUnconfigureAaaAuthorization(unittest.TestCase):

    def test_unconfigure_network(self):
        device = Mock()
        unconfigure_aaa_authorization(device, 'network', 'default', ['group RADIUS_GRP', 'local'])
        device.configure.assert_called_once_with(
            'no aaa authorization network default group RADIUS_GRP local'
        )

    def test_unconfigure_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_aaa_authorization(device, 'network', 'default', ['group RADIUS_GRP', 'local'])


if __name__ == '__main__':
    unittest.main()
