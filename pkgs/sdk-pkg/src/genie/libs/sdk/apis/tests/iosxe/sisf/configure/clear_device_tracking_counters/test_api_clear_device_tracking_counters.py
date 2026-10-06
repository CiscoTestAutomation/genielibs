from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sisf.configure import (
    clear_device_tracking_counters,
)


class TestClearDeviceTrackingCounters(TestCase):

    def test_clear_device_tracking_counters(self):
        device = Mock()

        result = clear_device_tracking_counters(device=device)

        self.assertIsNone(result)
        device.execute.assert_called_once_with(
            'clear device-tracking counters',
        )

    def test_clear_device_tracking_counters_1(self):
        device = Mock()

        result = clear_device_tracking_counters(
            device=device,
            interface='Ethernet1/0',
        )

        self.assertIsNone(result)
        device.execute.assert_called_once_with(
            'clear device-tracking counters interface Ethernet1/0',
        )

    def test_clear_device_tracking_counters_2(self):
        device = Mock()

        result = clear_device_tracking_counters(device=device, vlan='200')

        self.assertIsNone(result)
        device.execute.assert_called_once_with(
            'clear device-tracking counters vlan 200',
        )

    def test_clear_device_tracking_counters_3(self):
        device = Mock()

        result = clear_device_tracking_counters(device=device, bdi='200')

        self.assertIsNone(result)
        device.execute.assert_called_once_with(
            'clear device-tracking counters bdi 200',
        )
