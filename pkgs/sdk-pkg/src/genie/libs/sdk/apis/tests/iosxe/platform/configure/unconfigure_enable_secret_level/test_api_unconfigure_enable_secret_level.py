import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_enable_secret_level


class TestUnconfigureEnableSecretLevel(unittest.TestCase):

    def test_unconfigure_enable_secret_level(self):
        device = Mock()

        result = unconfigure_enable_secret_level(device, 5)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no enable secret level 5',)
        )