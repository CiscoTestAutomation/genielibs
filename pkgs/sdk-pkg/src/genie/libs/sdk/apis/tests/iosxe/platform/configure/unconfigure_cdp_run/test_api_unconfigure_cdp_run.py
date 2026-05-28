import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_cdp_run


class TestUnconfigureCdpRun(unittest.TestCase):

    def test_unconfigure_cdp_run(self):
        device = Mock()

        result = unconfigure_cdp_run(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no cdp run',)
        )