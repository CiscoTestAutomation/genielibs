from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import config_cns_agent_passwd


class TestConfigCnsAgentPasswd(TestCase):

    def test_config_cns_agent_passwd(self):
        device = Mock()
        result = config_cns_agent_passwd(
            device,
            'sharath'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('cns password sharath',)
        )