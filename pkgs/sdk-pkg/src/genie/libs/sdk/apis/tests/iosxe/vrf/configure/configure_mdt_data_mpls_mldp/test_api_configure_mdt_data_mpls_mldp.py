import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    configure_mdt_data_mpls_mldp,
)


class TestConfigureMdtDataMplsMldp(unittest.TestCase):

    def test_configure_mdt_data_mpls_mldp(self):
        device = Mock()

        result = configure_mdt_data_mpls_mldp(
            device=device,
            vrf_name='vrf3001',
            address_family='ipv4',
            mdt_data=10,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition vrf3001',
                'address-family ipv4',
                'mdt data mpls mldp 10',
            ]
        )
