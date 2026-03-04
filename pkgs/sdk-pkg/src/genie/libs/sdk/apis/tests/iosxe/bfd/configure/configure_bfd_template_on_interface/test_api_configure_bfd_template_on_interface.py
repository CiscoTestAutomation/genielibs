from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import configure_bfd_template_on_interface
from unittest.mock import Mock


class TestConfigureBfdTemplateOnInterface(TestCase):

    def test_configure_bfd_template_on_interface(self):
        self.device = Mock()
        self.device.configure.return_value = None

        result = configure_bfd_template_on_interface(self.device, 'GigabitEthernet1/0/1', 'test_template')

        self.device.configure.assert_called_once_with([
            'interface GigabitEthernet1/0/1',
            'bfd template test_template'
        ])

        expected_output = None
        self.assertEqual(result, expected_output)
