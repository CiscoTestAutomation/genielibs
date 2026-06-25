import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_qfp_drop_threshold


class TestUnconfigureQfpDropThreshold(unittest.TestCase):

    def test_unconfigure_qfp_drop_threshold_percause(self):
        device = Mock()

        result = unconfigure_qfp_drop_threshold(
            device,
            10,
            drop_id=2
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no platform qfp drops threshold per-cause 2 10',)
        )

    def test_unconfigure_qfp_drop_threshold_total(self):
        device = Mock()

        result = unconfigure_qfp_drop_threshold(
            device,
            20
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no platform qfp drops threshold total 20',)
        )