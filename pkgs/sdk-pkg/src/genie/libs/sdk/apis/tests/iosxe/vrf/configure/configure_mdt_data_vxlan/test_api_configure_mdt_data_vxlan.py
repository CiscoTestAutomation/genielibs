import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import configure_mdt_data_vxlan


class TestConfigureMdtDataVxlan(unittest.TestCase):

    def test_configure_mdt_data_vxlan(self):
        device = Mock()

        result = configure_mdt_data_vxlan(
            device,
            'red',
            'ipv4',
            '228.0.0.0',
            '0.0.0.0',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition red',
                'address-family ipv4',
                'mdt data vxlan 228.0.0.0 0.0.0.0',
            ]
        )
