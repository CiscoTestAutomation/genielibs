from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.span.configure import (
    unconfigure_local_span_filter,
)


class TestUnconfigureLocalSpanFilter(TestCase):

    def test_unconfigure_local_span_filter(self):
        device = Mock()

        result = unconfigure_local_span_filter(
            device,
            '1',
            'vlan',
            '',
            '1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                'no monitor session 1 filter vlan 1',
            )
        )
