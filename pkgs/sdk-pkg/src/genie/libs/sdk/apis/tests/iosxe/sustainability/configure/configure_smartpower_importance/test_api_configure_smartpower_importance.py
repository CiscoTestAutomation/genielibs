from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    configure_smartpower_importance,
)


class TestConfigureSmartpowerImportance(TestCase):

    def test_configure_smartpower_importance(self):
        device = Mock()

        result = configure_smartpower_importance(device, '10')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'smartpower importance 10'
        )
