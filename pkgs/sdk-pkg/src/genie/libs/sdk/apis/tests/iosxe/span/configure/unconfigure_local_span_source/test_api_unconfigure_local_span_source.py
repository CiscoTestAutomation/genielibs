from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.span.configure import (
    unconfigure_local_span_source,
)


class TestUnconfigureLocalSpanSource(TestCase):

    def test_unconfigure_local_span_source(self):
        device = Mock()

        result = unconfigure_local_span_source(
            device,
            1,
            'interface',
            'te1/0/5',
            'rx'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no monitor session 1 source interface te1/0/5 rx\n',)
        )
