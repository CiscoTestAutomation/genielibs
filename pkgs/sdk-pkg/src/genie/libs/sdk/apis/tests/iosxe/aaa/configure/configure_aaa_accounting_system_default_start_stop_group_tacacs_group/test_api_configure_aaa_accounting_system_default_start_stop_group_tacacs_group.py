from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_accounting_system_default_start_stop_group_tacacs_group
from unittest.mock import Mock


class TestConfigureAaaAccountingSystemDefaultStartStopGroupTacacsGroup(TestCase):

    def test_configure_aaa_accounting_system_default_start_stop_group_tacacs_group(self):
        self.device = Mock()
        configure_aaa_accounting_system_default_start_stop_group_tacacs_group(self.device, 'TACACS-group')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('aaa accounting system default start-stop group tacacs+ group TACACS-group',)
        )
 
