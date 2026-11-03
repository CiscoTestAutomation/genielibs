from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.nat.execute import (
    execute_clear_nat_translation,
)


class TestExecuteClearNatTranslation(TestCase):

    def test_execute_clear_nat_translation(self):
        device = Mock()
        device.execute.return_value = ''
        result = execute_clear_nat_translation(device)

        self.assertEqual(result, '')
        device.execute.assert_called_once_with('clear ip nat translation *')
