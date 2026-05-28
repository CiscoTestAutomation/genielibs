import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_enable_secret_password


class TestUnconfigureEnableSecretPassword(unittest.TestCase):

    def test_unconfigure_enable_secret_password(self):
        device = Mock()

        result = unconfigure_enable_secret_password(device, 'cisco@123', 5)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no enable secret level 5'],)
        )