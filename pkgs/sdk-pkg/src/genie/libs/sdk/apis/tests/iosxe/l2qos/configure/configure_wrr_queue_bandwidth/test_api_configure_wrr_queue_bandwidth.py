import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.l2qos.configure import (
    configure_wrr_queue_bandwidth,
)


class TestConfigureWrrQueueBandwidth(TestCase):

    def test_configure_wrr_queue_bandwidth_with_values(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_wrr_queue_bandwidth(
            device, bandwidth=[1, 2, 3, 6, 12, 17, 25, 33])

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "wrr-queue bandwidth 1 2 3 6 12 17 25 33")

    def test_configure_wrr_queue_bandwidth_default(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_wrr_queue_bandwidth(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with("wrr-queue bandwidth")


if __name__ == "__main__":
    unittest.main()
