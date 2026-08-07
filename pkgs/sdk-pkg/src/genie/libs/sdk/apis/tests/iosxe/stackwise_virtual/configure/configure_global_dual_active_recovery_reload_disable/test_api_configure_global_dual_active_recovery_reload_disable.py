from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.stackwise_virtual.configure import (
    configure_global_dual_active_recovery_reload_disable,
)


class TestConfigureGlobalDualActiveRecoveryReloadDisable(TestCase):

    def test_configure_global_dual_active_recovery_reload_disable(self):
        device = Mock()
        device.configure.return_value = (
            'stackwise-virtual\r\n'
            'stackwise-virtual\r\n'
            'dual-active recovery-reload-disable\r\n'
            'Please reload the switch for Stackwise Virtual configuration to take '
            'effect\r\n'
        )

        result = configure_global_dual_active_recovery_reload_disable(device)

        self.assertEqual(
            result,
            (
                'stackwise-virtual\r\n'
                'stackwise-virtual\r\n'
                'dual-active recovery-reload-disable\r\n'
                'Please reload the switch for Stackwise Virtual configuration to take '
                'effect\r\n'
            )
        )
        device.configure.assert_called_once_with(
            [
                'stackwise-virtual',
                'dual-active recovery-reload-disable',
            ]
        )
