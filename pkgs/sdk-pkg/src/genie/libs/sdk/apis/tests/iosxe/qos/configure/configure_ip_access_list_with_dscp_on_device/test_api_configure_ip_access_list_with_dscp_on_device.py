import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.qos.configure import (
    configure_ip_access_list_with_dscp_on_device
)


class TestConfigureIpAccessListWithDscpOnDevice(unittest.TestCase):

    def test_configure_ip_access_list_with_dscp_on_device(self):
        device = Mock()

        result = configure_ip_access_list_with_dscp_on_device(
            device,
            100,
            10,
            'permit',
            '131.1.1.2',
            '162.1.1.2',
            '7'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip access-list extended 100',
              '10 permit ip host 131.1.1.2 host 162.1.1.2 dscp 7'],)
        )