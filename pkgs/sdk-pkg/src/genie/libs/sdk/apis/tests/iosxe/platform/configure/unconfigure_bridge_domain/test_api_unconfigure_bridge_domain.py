import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_bridge_domain


class TestUnconfigureBridgeDomain(unittest.TestCase):

    def test_unconfigure_bridge_domain(self):
        device = Mock()

        result = unconfigure_bridge_domain(device, '50')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no bridge-domain 50'],)
        )