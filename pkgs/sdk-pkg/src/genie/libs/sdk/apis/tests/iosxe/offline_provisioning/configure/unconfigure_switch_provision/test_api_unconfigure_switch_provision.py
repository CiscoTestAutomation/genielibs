from unittest import TestCase
from genie.libs.sdk.apis.iosxe.offline_provisioning.configure import unconfigure_switch_provision
from unittest.mock import Mock


class TestUnconfigureSwitchProvision(TestCase):

    def test_unconfigure_switch_provision(self):
        self.device = Mock()
        result = unconfigure_switch_provision(self.device, '3', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no switch 3 provision',)
        )
