import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.l2qos.configure import (
    unconfigure_wrr_queue_cos_map,
)


class TestUnconfigureWrrQueueCosMap(TestCase):

    def test_unconfigure_wrr_queue_cos_map(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_wrr_queue_cos_map(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with("no wrr-queue cos-map")


if __name__ == "__main__":
    unittest.main()
