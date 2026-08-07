from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.span.configure import (
    unconfigure_local_span_destination_interface,
)


class TestUnconfigureLocalSpanDestinationInterface(TestCase):

    def test_unconfigure_local_span_destination_interface(self):
        device = Mock()

        result = unconfigure_local_span_destination_interface(
            device,
            1,
            'vlan',
            '5'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no monitor session 1 destination remote vlan 5\n',)
        )
