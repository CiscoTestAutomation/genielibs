import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_ip_local_pool


class TestUnconfigureIpLocalPool(unittest.TestCase):

    def test_unconfigure_ip_local_pool(self):
        device = Mock()

        result = unconfigure_ip_local_pool(device, 'ipv4_pool')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip local pool ipv4_pool',)
        )