from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.span.configure import (
    configure_local_span_destination,
)


class TestConfigureLocalSpanDestination(TestCase):

    def test_configure_local_span_destination(self):
        device = Mock()

        result = configure_local_span_destination(
            device,
            10,
            'Gi1/0/4',
            'dot1q',
            'vlan',
            100,
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                'monitor session 10 destination interface Gi1/0/4 encapsulation dot1q ingress vlan 100\n',
            )
        )
