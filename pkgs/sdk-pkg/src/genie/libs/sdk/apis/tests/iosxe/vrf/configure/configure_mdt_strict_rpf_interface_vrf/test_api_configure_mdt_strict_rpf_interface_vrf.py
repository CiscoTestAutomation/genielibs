import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    configure_mdt_strict_rpf_interface_vrf,
)


class TestConfigureMdtStrictRpfInterfaceVrf(unittest.TestCase):

    def test_configure_mdt_strict_rpf_interface_vrf(self):
        device = Mock()

        result = configure_mdt_strict_rpf_interface_vrf(
            device=device,
            vrf='vrf3001',
            address_family='ipv4',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition vrf3001',
                'address-family ipv4',
                'mdt strict-rpf interface',
            ]
        )
