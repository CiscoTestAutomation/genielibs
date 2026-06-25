import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_macro_auto_global_processing_on_interface


class TestUnconfigureMacroAutoGlobalProcessingOnInterface(unittest.TestCase):

    def test_unconfigure_macro_auto_global_processing_on_interface(self):
        device = Mock()

        result = unconfigure_macro_auto_global_processing_on_interface(device, 'te1/0/1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface te1/0/1','no macro auto global processing'],)
        )