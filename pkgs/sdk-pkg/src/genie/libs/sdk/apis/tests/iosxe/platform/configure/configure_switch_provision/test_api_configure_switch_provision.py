from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_switch_provision

class TestConfigureSwitchProvision(TestCase):

    def test_configure_switch_provision(self):
        device = Mock()
        result = configure_switch_provision(device, 2, 'c9300-24h')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('switch 2 provision c9300-24h',)
        )