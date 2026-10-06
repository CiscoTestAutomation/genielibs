from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.running_config.verify import \
    verify_show_running_config_section


class TestVerifyShowRunningConfigSection(TestCase):
    def setUp(self):
        self.device = Mock()
        self.device.execute.return_value = (
            'switchport access vlan 100\n'
            'switchport mode access\n'
            'switchport\n'
        )

    def test_verify_show_running_config_section(self):
        result = verify_show_running_config_section(
            self.device,
            section='switchport',
            expect_list=['switchport mode access',
                         'switchport access vlan 100'],
            unexpect_list=['switchport mode trunk']
        )
        self.assertTrue(result)

        self.device.execute.assert_called_once_with(
            'show running-config | section switchport'
        )

    def test_verify_show_running_config_no_unexpect(self):
        result = verify_show_running_config_section(
            self.device,
            section='switchport',
            expect_list=['switchport mode trunk',
                         'switchport access vlan 100'],
        )
        self.assertFalse(result)

        self.device.execute.assert_called_once_with(
            'show running-config | section switchport'
        )
