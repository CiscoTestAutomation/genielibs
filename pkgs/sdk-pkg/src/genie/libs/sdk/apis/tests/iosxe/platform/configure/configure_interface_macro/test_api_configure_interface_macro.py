import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_interface_macro


class TestConfigureInterfaceMacro(unittest.TestCase):

    def test_configure_interface_macro(self):
        device = Mock()

        result = configure_interface_macro(device, 'te1/0/2', 'hello-cisco')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface te1/0/2', 'macro apply hello-cisco'],)
        )