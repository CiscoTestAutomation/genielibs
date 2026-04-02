from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ie9k.platform.get import get_boot_variables


class TestGetBootVariables(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.device = Mock()

    def test_get_current_boot_variable_from_current(self):
        self.device.parse.return_value = {
            'current_boot_variable': 'bootflash:iosxe-image.bin;'
        }

        result = get_boot_variables(self.device, 'current')

        self.device.parse.assert_called_with('show boot', output=None)
        self.assertEqual(result, ['bootflash:iosxe-image.bin'])
