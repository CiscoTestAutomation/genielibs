import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_mdix_auto


class TestConfigureMdixAuto(unittest.TestCase):

    def test_configure_mdix_auto(self):
        device = Mock()

        result = configure_mdix_auto(device, 'te1/0/1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface te1/0/1', 'mdix auto'],)
        )