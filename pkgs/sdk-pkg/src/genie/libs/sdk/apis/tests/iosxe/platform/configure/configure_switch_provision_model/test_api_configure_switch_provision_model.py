import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_switch_provision_model


class TestConfigureSwitchProvisionModel(unittest.TestCase):

    def test_configure_switch_provision_model(self):
        device = Mock()

        result = configure_switch_provision_model(device, '1', 'c9300-48u')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('switch 1 provision c9300-48u',)
        )