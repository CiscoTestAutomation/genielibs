import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.rip.configure import (
    clear_ipv6_rip
)


class TestClearIpv6Rip(unittest.TestCase):

    def test_clear_ipv6_rip(self):
        device = Mock()

        result = clear_ipv6_rip(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('clear ipv6 rip',)
        )