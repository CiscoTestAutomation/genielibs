from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.stackwise_virtual.configure import (
    unconfigure_stackwise_virtual_dual_active_interfaces,
)


class TestUnconfigureStackwiseVirtualDualActiveInterfaces(TestCase):

    def test_unconfigure_stackwise_virtual_dual_active_interfaces(self):
        device = Mock()
        expected_output = (
            'interface HundredGigE1/0/7\r\n'
            'interface HundredGigE1/0/7\r\n'
            'no stackwise-virtual dual-active-detection\r\n'
            'no stackwise-virtual dual-active-detection\r\n'
        )
        device.configure.return_value = expected_output

        result = unconfigure_stackwise_virtual_dual_active_interfaces(
            device,
            ['HundredGigE1/0/7']
        )

        self.assertEqual(result, expected_output)
        device.configure.assert_called_once_with(
            [
                'interface HundredGigE1/0/7',
                'no stackwise-virtual dual-active-detection',
            ]
        )
