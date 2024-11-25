import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_tacacs_group


class TestUnconfigureTacacsGroup(unittest.TestCase):

    def test_unconfigure_tacacs_group(self):
        self.device = Mock()
        unconfigure_tacacs_group(self.device, 'Test')
        self.device.configure.assert_called_with(
            'no aaa group server tacacs Test'
        )
