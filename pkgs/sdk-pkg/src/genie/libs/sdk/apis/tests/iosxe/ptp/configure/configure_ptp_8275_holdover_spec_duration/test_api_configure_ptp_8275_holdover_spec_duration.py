import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ptp.configure import (
    configure_ptp_8275_holdover_spec_duration
)


class TestConfigurePtp8275HoldoverSpecDuration(unittest.TestCase):

    def test_configure_ptp_8275_holdover_spec_duration(self):
        device = Mock()

        result = configure_ptp_8275_holdover_spec_duration(
            device=device,
            holdover='1000'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ptp holdover 8275.1 spec-duration 1000'],)
        )