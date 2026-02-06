from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cts.configure import clear_cts_counters_ipv6


class TestClearCtsCountersIpv6(TestCase):
    def test_clear_cts_counters_ipv6(self):
        device = Mock()
        result = clear_cts_counters_ipv6(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('clear cts role-based counters ipv6',)
        )