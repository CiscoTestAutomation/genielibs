from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.stackwise_virtual.configure import (
    unconfigure_stackwise_virtual_dual_active_pagp,
)


class TestUnconfigureStackwiseVirtualDualActivePagp(TestCase):

    def test_unconfigure_stackwise_virtual_dual_active_pagp(self):
        device = Mock()
        expected_output = (
            'stackwise-virtual\r\n'
            'stackwise-virtual\r\n'
            'no dual-active detection pagp trust channel-group 1\r\n'
            'Please reload the switch for Stackwise Virtual configuration to take '
            'effect\r\n'
        )
        device.configure.return_value = expected_output

        result = unconfigure_stackwise_virtual_dual_active_pagp(
            device,
            '1'
        )

        self.assertEqual(result, expected_output)
        device.configure.assert_called_once_with(
            [
                'stackwise-virtual',
                'no dual-active detection pagp trust channel-group 1',
            ]
        )
