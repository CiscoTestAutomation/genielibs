import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import configure_vpn_id_in_vrf


class TestConfigureVpnIdInVrf(unittest.TestCase):

    def test_configure_vpn_id_in_vrf(self):
        device = Mock()

        result = configure_vpn_id_in_vrf(
            device=device,
            vrf_name='vrf3001',
            vpn_id='3001:1',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition vrf3001',
                'vpn id 3001:1',
            ]
        )
