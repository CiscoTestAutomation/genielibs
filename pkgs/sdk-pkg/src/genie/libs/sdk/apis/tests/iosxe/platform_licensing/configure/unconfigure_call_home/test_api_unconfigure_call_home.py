import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import unconfigure_call_home


class TestUnconfigureCallHome(unittest.TestCase):

    def test_unconfigure_call_home(self):
        device = Mock()

        result = unconfigure_call_home(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no call-home',)
        )