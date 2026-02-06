from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cdp.configure import unconfigure_cdp_timer


class TestUnconfigureCdpTimer(TestCase):

    def test_unconfigure_cdp_timer(self):
        device = Mock()
        result = unconfigure_cdp_timer(device)
        expected_output = None
        self.assertEqual(result, expected_output)

        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no cdp timer'],)
        )


if __name__ == '__main__':
    import unittest
    unittest.main()