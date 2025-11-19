import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import  configure_disable_aes_encryption

class TestAesEncryption(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "Router1"

    
    def test_disable_with_new_key(self):
        configure_disable_aes_encryption(
            device=self.device,
            new_key="CiscoKey1234"
        )