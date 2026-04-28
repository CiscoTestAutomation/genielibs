from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import clear_macro_auto_confgis


class TestClearMacroAutoConfgis(TestCase):

    def test_clear_macro_auto_confgis(self):
        device = Mock()
        result = clear_macro_auto_confgis(
            device,
            ''
        )
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('clear macro auto configuration all',)
        )