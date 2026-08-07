from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    configure_smartpower_domain,
)


class TestConfigureSmartpowerDomain(TestCase):

    def test_configure_smartpower_domain(self):
        device = Mock()

        result = configure_smartpower_domain(
            device,
            'cisco',
            'shared-secret',
            'cisco123',
            'udp',
            '43440'
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'smartpower domain cisco security shared-secret cisco123 protocol udp port 43440'
        )
