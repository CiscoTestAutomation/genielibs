import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_call_home


class TestConfigureCallHome(unittest.TestCase):

    def test_configure_call_home(self):
        device = Mock()

        result = configure_call_home(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('call-home',)
        )