import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_mdix_auto


class TestUnconfigureMdixAuto(unittest.TestCase):

    def test_unconfigure_mdix_auto(self):
        device = Mock()

        result = unconfigure_mdix_auto(device, 'te1/0/1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface te1/0/1','no mdix auto'],)
        )