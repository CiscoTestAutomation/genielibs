from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.stackwise_virtual.configure import (
    configure_global_stackwise_virtual,
)


class TestConfigureGlobalStackwiseVirtual(TestCase):

    def test_configure_global_stackwise_virtual(self):
        device = Mock()
        device.configure.return_value = (
            'stackwise-virtual\r\n'
            'stackwise-virtual\r\n'
            'domain 1\r\n'
            'Please reload the switch for Stackwise Virtual configuration to take '
            'effect\r\n'
        )

        result = configure_global_stackwise_virtual(device, 1)

        self.assertEqual(
            result,
            (
                'stackwise-virtual\r\n'
                'stackwise-virtual\r\n'
                'domain 1\r\n'
                'Please reload the switch for Stackwise Virtual configuration to take '
                'effect\r\n'
            )
        )
        device.configure.assert_called_once_with(
            [
                'stackwise-virtual',
                'domain 1',
            ]
        )
