import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_line_vty


class TestUnconfigureLineVty(unittest.TestCase):

    def test_unconfigure_line_vty(self):
        device = Mock()

        result = unconfigure_line_vty(device, '1', '2')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no line vty 1 2',)
        )