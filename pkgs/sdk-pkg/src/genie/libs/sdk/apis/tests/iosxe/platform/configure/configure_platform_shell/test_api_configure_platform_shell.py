import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_platform_shell


class TestConfigurePlatformShell(unittest.TestCase):

    def test_configure_platform_shell(self):
        device = Mock()

        result = configure_platform_shell(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('platform shell',)
        )