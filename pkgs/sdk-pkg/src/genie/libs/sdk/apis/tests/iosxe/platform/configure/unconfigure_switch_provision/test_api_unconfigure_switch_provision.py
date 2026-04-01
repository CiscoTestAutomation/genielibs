from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_switch_provision

class TestUnconfigureSwitchProvision(TestCase):

    def test_unconfigure_switch_provision(self):
        device = Mock()
        result = unconfigure_switch_provision(device, 2)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no switch 2 provision',)
        )