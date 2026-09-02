import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    configure_mdt_auto_discovery_inter_as_mdt_type,
)


class TestConfigureMdtAutoDiscoveryInterAsMdtType(unittest.TestCase):

    def test_configure_mdt_auto_discovery_inter_as_mdt_type(self):
        device = Mock()

        result = configure_mdt_auto_discovery_inter_as_mdt_type(
            device,
            'green',
            'ipv4',
            'interworking',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition green',
                'address-family ipv4',
                'mdt auto-discovery interworking vxlan-pim inter-as',
            ]
        )
