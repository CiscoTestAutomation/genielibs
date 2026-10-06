from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sisf.configure import (
    unconfigure_device_tracking_binding,
)


class TestUnconfigureDeviceTrackingBinding(TestCase):

    def test_unconfigure_device_tracking_binding(self):
        device = Mock()
        result = unconfigure_device_tracking_binding(
            device=device,
            vlan=10,
            address='10.10.10.10',
            interface='te1/0/1',
            mac='dead.beef.1000',
            tracking='default',
        )
        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no device-tracking binding vlan 10 10.10.10.10 '
            'interface te1/0/1 dead.beef.1000 tracking default'
        )
