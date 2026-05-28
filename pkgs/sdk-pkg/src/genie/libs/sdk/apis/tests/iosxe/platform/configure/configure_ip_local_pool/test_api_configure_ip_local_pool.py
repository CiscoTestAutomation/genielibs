import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_local_pool


class TestConfigureIpLocalPool(unittest.TestCase):

    def test_configure_ip_local_pool(self):
        device = Mock()

        result = configure_ip_local_pool(device, 'pool1', '1.1.1.1', '1.1.1.10')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip local pool pool1 1.1.1.1 1.1.1.10',)
        )