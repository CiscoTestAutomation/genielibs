import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ptp.configure import (
    unconfigure_ptp_neighbor_propagation_delay_threshold
)


class TestUnconfigurePtpNeighborPropagationDelayThreshold(unittest.TestCase):

    def test_unconfigure_ptp_neighbor_propagation_delay_threshold(self):
        device = Mock()

        result = unconfigure_ptp_neighbor_propagation_delay_threshold(
            device
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
             (['no ptp neighbor-propagation-delay-threshold'],)
        )