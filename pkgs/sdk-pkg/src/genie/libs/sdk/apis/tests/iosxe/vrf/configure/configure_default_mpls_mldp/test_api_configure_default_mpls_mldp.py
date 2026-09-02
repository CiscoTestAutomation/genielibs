import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import configure_default_mpls_mldp


class TestConfigureDefaultMplsMldp(unittest.TestCase):

    def test_configure_default_mpls_mldp(self):
        device = Mock()

        result = configure_default_mpls_mldp(
            device,
            'vrf3001',
            'ipv4',
            '5.5.5.5',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition vrf3001',
                'address-family ipv4',
                'mdt default mpls mldp  5.5.5.5',
            ]
        )
