from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.span.configure import (
    configure_local_span_source,
)


class TestConfigureLocalSpanSource(TestCase):

    def test_configure_local_span_source(self):
        device = Mock()

        result = configure_local_span_source(
            device,
            1,
            'interface',
            'te1/0/5',
            'rx'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('monitor session 1 source interface te1/0/5 rx\n',)
        )
