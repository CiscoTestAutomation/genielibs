import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ptp.configure import (
    unconfigure_ptp_8275_holdover_spec_duration
)


class TestUnconfigurePtp8275HoldoverSpecDuration(unittest.TestCase):

    def test_unconfigure_ptp_8275_holdover_spec_duration(self):
        device = Mock()

        result = unconfigure_ptp_8275_holdover_spec_duration(
            device=device
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ptp holdover 8275.1 spec-duration',)
        )