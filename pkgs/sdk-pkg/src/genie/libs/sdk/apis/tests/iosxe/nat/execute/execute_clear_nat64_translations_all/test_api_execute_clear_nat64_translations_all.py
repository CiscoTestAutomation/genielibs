from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.nat.execute import (
    execute_clear_nat64_translations_all,
)


class TestExecuteClearNat64TranslationsAll(TestCase):

    def test_execute_clear_nat64_translations_all(self):
        device = Mock()
        result = execute_clear_nat64_translations_all(device)

        self.assertIsNone(result)
        device.execute.assert_called_once_with(
            'clear nat64 translations all'
        )
