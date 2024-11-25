import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_tacacs_server


class TestUnconfigureTacacsServer(unittest.TestCase):

    def test_unconfigure_tacacs_server(self):
        self.device = Mock()
        result = unconfigure_tacacs_server(self.device, 'Test')
        self.device.configure.assert_called_with(
            'no tacacs server Test'
        )
