import unittest
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.span.configure import (
    configure_local_span_source_and_get_output)


class TestConfigureLocalSpanSourceAndGetOutput(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_configure_local_span_source_interface_with_direction(self):
        self.device.configure.return_value = "  some output  "
        result = configure_local_span_source_and_get_output(
            self.device, 1, 'interface', 'te1/0/5', 'rx')
        self.device.configure.assert_called_once_with(
            "monitor session 1 source interface te1/0/5 rx\n")
        self.assertEqual(result, "some output")

    def test_configure_local_span_source_vlan_no_direction(self):
        self.device.configure.return_value = ""
        result = configure_local_span_source_and_get_output(
            self.device, 2, 'vlan', '100')
        self.device.configure.assert_called_once_with(
            "monitor session 2 source vlan 100")
        self.assertEqual(result, "")

    def test_configure_local_span_source_invalid_int_type(self):
        with self.assertRaises(ValueError):
            configure_local_span_source_and_get_output(
                self.device, 1, 'bogus', 'te1/0/5')
        self.device.configure.assert_not_called()

    def test_configure_local_span_source_subcommand_failure(self):
        self.device.configure.side_effect = SubCommandFailure("boom")
        with self.assertRaises(SubCommandFailure):
            configure_local_span_source_and_get_output(
                self.device, 1, 'interface', 'te1/0/5', 'rx')


if __name__ == '__main__':
    unittest.main()
