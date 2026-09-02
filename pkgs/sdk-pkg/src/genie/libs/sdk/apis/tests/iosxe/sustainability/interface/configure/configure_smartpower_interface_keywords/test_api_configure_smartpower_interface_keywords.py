from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.interface.configure import (
    configure_smartpower_interface_keywords,
)


class TestConfigureSmartpowerInterfaceKeywords(TestCase):

    def test_configure_smartpower_interface_keywords(self):
        device = Mock()

        result = configure_smartpower_interface_keywords(
            device,
            'Gi1/0/13',
            'potato',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ['interface Gi1/0/13', 'smartpower keywords potato']
        )
