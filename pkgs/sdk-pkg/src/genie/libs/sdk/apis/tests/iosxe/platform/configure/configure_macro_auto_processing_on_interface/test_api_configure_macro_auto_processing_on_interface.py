import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_macro_auto_processing_on_interface


class TestConfigureMacroAutoProcessingOnInterface(unittest.TestCase):

    def test_configure_macro_auto_processing_on_interface(self):
        device = Mock()

        result = configure_macro_auto_processing_on_interface(device, 'te1/0/1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface te1/0/1', 'macro auto processing'],)
        )