import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.l2qos.configure import (
    unconfigure_wrr_queue_bandwidth,
)


class TestUnconfigureWrrQueueBandwidth(TestCase):

    def test_unconfigure_wrr_queue_bandwidth(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_wrr_queue_bandwidth(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with("no wrr-queue bandwidth")


if __name__ == "__main__":
    unittest.main()
