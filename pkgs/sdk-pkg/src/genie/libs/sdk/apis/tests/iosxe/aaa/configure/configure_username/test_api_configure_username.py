import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_username


class TestConfigureUsername(unittest.TestCase):

    def test_configure_username(self):
        self.device = Mock()
        configure_username(self.device, 'test', 'lab', 0, '1')
        self.device.configure.assert_called_once_with(
            'username test privilege 1 password lab'
        )
