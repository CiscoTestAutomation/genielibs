from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.stackwise_virtual.configure import (
    configure_stackwise_virtual_dual_active_interfaces,
)


class TestConfigureStackwiseVirtualDualActiveInterfaces(TestCase):

    def test_configure_stackwise_virtual_dual_active_interfaces(self):
        device = Mock()
        device.configure.return_value = (
            'interface HundredGigE1/0/7\r\n'
            'interface HundredGigE1/0/7\r\n'
            'stackwise-virtual dual-active-detection\r\n'
            'stackwise-virtual dual-active-detection\r\n'
        )

        result = configure_stackwise_virtual_dual_active_interfaces(
            device,
            ['HundredGigE1/0/7']
        )

        self.assertEqual(
            result,
            (
                'interface HundredGigE1/0/7\r\n'
                'interface HundredGigE1/0/7\r\n'
                'stackwise-virtual dual-active-detection\r\n'
                'stackwise-virtual dual-active-detection\r\n'
            )
        )
        device.configure.assert_called_once_with(
            [
                'interface HundredGigE1/0/7',
                'stackwise-virtual dual-active-detection',
            ]
        )
