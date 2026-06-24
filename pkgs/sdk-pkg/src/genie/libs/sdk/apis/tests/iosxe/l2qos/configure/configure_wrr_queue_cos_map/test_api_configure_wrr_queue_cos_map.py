import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.l2qos.configure import (
    configure_wrr_queue_cos_map,
)


class TestConfigureWrrQueueCosMap(TestCase):

    def test_configure_wrr_queue_cos_map(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_wrr_queue_cos_map(
            device, queue_id=1, cos_list=[0, 1])

        self.assertIsNone(result)
        device.configure.assert_called_once_with("wrr-queue cos-map 1 0 1")


if __name__ == "__main__":
    unittest.main()
