from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.stackwise_virtual.configure import (
    configure_stackwise_virtual_dual_active_pagp,
)


class TestConfigureStackwiseVirtualDualActivePagp(TestCase):

    def test_configure_stackwise_virtual_dual_active_pagp(self):
        device = Mock()
        device.configure.return_value = (
            'stackwise-virtual\r\n'
            'stackwise-virtual\r\n'
            'dual-active detection pagp\r\n'
            'Please reload the switch for Stackwise Virtual configuration to take '
            'effect\r\n'
            'dual-active detection pagp trust channel-group 1\r\n'
            'Upon reboot, the config will be part of running config but not part of start '
            'up config.\r\n'
        )

        result = configure_stackwise_virtual_dual_active_pagp(
            device,
            '1'
        )

        self.assertEqual(
            result,
            (
                'stackwise-virtual\r\n'
                'stackwise-virtual\r\n'
                'dual-active detection pagp\r\n'
                'Please reload the switch for Stackwise Virtual configuration to take '
                'effect\r\n'
                'dual-active detection pagp trust channel-group 1\r\n'
                'Upon reboot, the config will be part of running config but not part of start '
                'up config.\r\n'
            )
        )
        device.configure.assert_called_once_with(
            [
                'stackwise-virtual',
                'dual-active detection pagp',
                'dual-active detection pagp trust channel-group 1',
            ]
        )
