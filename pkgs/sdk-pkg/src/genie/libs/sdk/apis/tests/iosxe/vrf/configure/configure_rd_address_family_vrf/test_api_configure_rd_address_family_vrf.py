import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    configure_rd_address_family_vrf,
)


class TestConfigureRdAddressFamilyVrf(unittest.TestCase):

    def test_configure_rd_address_family_vrf(self):
        device = Mock()

        result = configure_rd_address_family_vrf(
            device,
            'red',
            '2.2.2.2:33',
            'ipv6',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition red',
                'rd 2.2.2.2:33',
                'address-family ipv6',
            ]
        )
