from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.configure_mpls_mtu.configure import configure_mpls_mtu


class TestConfigureMplsMtu(TestCase):

    def test_configure_mpls_mtu(self):
        device = Mock()
        result = configure_mpls_mtu(device, 'HundredGigE1/0/26', '1400')
        expected_output = None
        self.assertEqual(result, expected_output)

        # Verify configure was called with the correct commands
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface HundredGigE1/0/26', 'mpls mtu 1400'],)
        )


if __name__ == '__main__':
    import unittest
    unittest.main()