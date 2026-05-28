import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_qfp_drop_threshold


class TestConfigureQfpDropThreshold(unittest.TestCase):

    def test_configure_qfp_drop_threshold_percause(self):
        device = Mock()

        result = configure_qfp_drop_threshold(device, 10, drop_id=2)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('platform qfp drops threshold per-cause 2 10',)
        )

    def test_configure_qfp_drop_threshold_total(self):
        device = Mock()

        result = configure_qfp_drop_threshold(device, 20)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('platform qfp drops threshold total 20',)
        )