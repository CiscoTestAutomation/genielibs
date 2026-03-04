from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import configure_bfd_template
from unittest.mock import Mock


class TestConfigureBfdTemplate(TestCase):

    def test_configure_bfd_template(self):
        self.device = Mock()
        self.device.configure.return_value = None

        result = configure_bfd_template(self.device, 'test_template', 100, 100, 3)

        self.device.configure.assert_called_once_with([
            'bfd-template single-hop test_template',
            'interval min-tx 100 min-rx 100 multiplier 3'
        ])

        expected_output = None
        self.assertEqual(result, expected_output)
