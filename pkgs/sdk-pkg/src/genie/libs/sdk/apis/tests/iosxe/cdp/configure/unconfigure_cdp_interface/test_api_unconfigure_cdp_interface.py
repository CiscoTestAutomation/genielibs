from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cdp.configure import unconfigure_cdp_interface


class TestUnconfigureCdpInterface(TestCase):

    def test_unconfigure_cdp_interface(self):
        device = Mock()
        result = unconfigure_cdp_interface(device, 'Te0/1/1')
        expected_output = None
        self.assertEqual(result, expected_output)

        # Verify configure was called with the correct commands
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Te0/1/1', 'no cdp enable', 'no cdp run'],)
        )

        device = Mock()
        result = unconfigure_cdp_interface(device, 'Te0/1/1', False)
        expected_output = None
        self.assertEqual(result, expected_output)

        # Verify configure was called with the correct commands
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Te0/1/1', 'no cdp enable'],)
        )

if __name__ == '__main__':
    import unittest
    unittest.main()