from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    configure_smartpower_role,
)


class TestConfigureSmartpowerRole(TestCase):

    def test_configure_smartpower_role(self):
        device = Mock()

        result = configure_smartpower_role(device, 'potato')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'smartpower role potato'
        )
