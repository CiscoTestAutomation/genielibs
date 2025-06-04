from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authentication_enable_default_group_enable
from unittest.mock import Mock


class TestConfigureAaaAccountingSystemDefaultStartStopGroupTacacsGroup(TestCase):

    def test_configure_aaa_authentication_enable_default_group_enable(self):
        self.device = Mock()
        configure_aaa_authentication_enable_default_group_enable(self.device, 'TACACS-group')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('aaa authentication enable default group TACACS-group enable',)
        )
 
