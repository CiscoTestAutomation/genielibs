import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authorization
from unicon.core.errors import SubCommandFailure


class TestConfigureAaaAuthorization(unittest.TestCase):

    def test_configure_network_group_local(self):
        device = Mock()
        configure_aaa_authorization(device, 'network', 'default', ['group RADIUS_GRP', 'local'])
        device.configure.assert_called_once_with(
            'aaa authorization network default group RADIUS_GRP local'
        )

    def test_configure_network_named_list(self):
        device = Mock()
        configure_aaa_authorization(device, 'network', 'AUTHOR_LIST', ['group RADIUS_GRP', 'local'])
        device.configure.assert_called_once_with(
            'aaa authorization network AUTHOR_LIST group RADIUS_GRP local'
        )

    def test_configure_subscriber_service(self):
        device = Mock()
        configure_aaa_authorization(device, 'subscriber-service', 'default', ['local', 'group RADIUS_GRP'])
        device.configure.assert_called_once_with(
            'aaa authorization subscriber-service default local group RADIUS_GRP'
        )

    def test_configure_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_aaa_authorization(device, 'network', 'default', ['group RADIUS_GRP', 'local'])


if __name__ == '__main__':
    unittest.main()
