from unittest import TestCase
from unittest.mock import ANY, Mock

from genie.libs.sdk.apis.iosxe.stackwise_virtual.configure import (
    unconfigure_stackwise_virtual_interfaces,
)


class TestUnconfigureStackwiseVirtualInterfaces(TestCase):

    def test_unconfigure_stackwise_virtual_interfaces(self):
        device = Mock()

        result = unconfigure_stackwise_virtual_interfaces(
            device,
            {'HundredGigE1/0/1': 1, 'HundredGigE1/0/10': 1},
            60
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface HundredGigE1/0/1',
                'no stackwise-virtual link 1',
                'interface HundredGigE1/0/10',
                'no stackwise-virtual link 1',
            ],
            reply=ANY,
            timeout=60,
            append_error_pattern=['.*Command cannot be executed.*']
        )
