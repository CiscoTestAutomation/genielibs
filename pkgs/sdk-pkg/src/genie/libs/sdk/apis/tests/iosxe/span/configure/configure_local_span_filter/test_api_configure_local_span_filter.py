from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.span.configure import (
    configure_local_span_filter,
)


class TestConfigureLocalSpanFilter(TestCase):

    def test_configure_local_span_filter(self):
        device = Mock()

        result = configure_local_span_filter(
            device,
            '1',
            'ip',
            '1',
            ''
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                'monitor session 1 filter ip access-group 1',
            )
        )
