from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cpp.configure import enable_cpp_system_default_on_device


class TestEnableCppSystemDefaultOnDevice(TestCase):
    def test_enable_cpp_system_default_on_device(self):
        device = Mock()
        result = enable_cpp_system_default_on_device(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['cpp system-default'],)
        )