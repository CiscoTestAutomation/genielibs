import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ptp.configure import (
    configure_ptp_neighbor_propagation_delay_threshold
)


class TestConfigurePtpNeighborPropagationDelayThreshold(unittest.TestCase):

    def test_configure_ptp_neighbor_propagation_delay_threshold(self):
        device = Mock()

        result = configure_ptp_neighbor_propagation_delay_threshold(
            device,
            '10'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ptp neighbor-propagation-delay-threshold 10'],)
        )