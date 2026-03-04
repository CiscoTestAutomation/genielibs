from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import unconfigure_bfd_template
from unittest.mock import Mock


class TestUnconfigureBfdTemplate(TestCase):

    def test_unconfigure_bfd_template(self):
        self.device = Mock()
        self.device.configure.return_value = None

        template_name = 'test_template'

        result = unconfigure_bfd_template(self.device, template_name)

        self.device.configure.assert_called_once_with('no bfd-template single-hop test_template')

        expected_output = None
        self.assertEqual(result, expected_output)
