from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    unconfigure_smartpower_domain,
)


class TestUnconfigureSmartpowerDomain(TestCase):

    def test_unconfigure_smartpower_domain(self):
        device = Mock()

        result = unconfigure_smartpower_domain(
            device,
            'cisco',
            'shared-secret',
            'cisco123',
            'udp',
            '1'
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no smartpower domain cisco security shared-secret cisco123 '
            'protocol udp port 1'
        )
