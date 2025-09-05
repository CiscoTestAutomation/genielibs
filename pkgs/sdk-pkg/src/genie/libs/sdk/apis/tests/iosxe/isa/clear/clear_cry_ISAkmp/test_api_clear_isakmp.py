import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.isa.clear import clear_cry_ISAkmp

class TestClearCryptoIsa(unittest.TestCase):

    def test_clear_isakmp_success(self):
        device = Mock()
        device.execute = Mock(return_value=None) 

        result = clear_cry_ISAkmp(device, timeout=10)

        self.assertIsNone(result)

        device.execute.assert_called_once_with('clear crypto isakmp', timeout=10)
