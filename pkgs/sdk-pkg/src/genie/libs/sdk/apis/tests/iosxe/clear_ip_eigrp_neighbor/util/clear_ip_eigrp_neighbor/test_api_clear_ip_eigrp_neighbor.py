from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.clear_ip_eigrp_neighbor.util import clear_ip_eigrp_neighbor


class TestClearIpEigrpNeighbor(TestCase):

    def test_clear_ip_eigrp_neighbor(self):
        device = Mock()
        result = clear_ip_eigrp_neighbor(device)
        expected_output = None
        self.assertEqual(result, expected_output)

        # Verify execute was called with the correct command
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('clear ip eigrp neighbor',)
        )


if __name__ == '__main__':
    import unittest
    unittest.main()