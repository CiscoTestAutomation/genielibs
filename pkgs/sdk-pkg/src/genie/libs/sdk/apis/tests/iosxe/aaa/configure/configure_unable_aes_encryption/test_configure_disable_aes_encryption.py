import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_enable_aes_encryption

class TestAesEncryption(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "Router1"

    def test_enable_proceed_without_old_key(self):
        configure_enable_aes_encryption(
            device=self.device,
            master_key="newStrongKey123",
            proceed_without_old_key=True
        )

        calls = [c[0][0] for c in self.device.configure.call_args_list]
        self.assertIn("key config-key password-encrypt", calls)
        self.assertIn("password encryption aes", calls)

