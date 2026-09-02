import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    configure_mdt_auto_discovery_vxlan,
)


class TestConfigureMdtAutoDiscoveryVxlan(unittest.TestCase):

    def test_configure_mdt_auto_discovery_vxlan(self):
        device = Mock()

        result = configure_mdt_auto_discovery_vxlan(
            device,
            'green',
            'ipv4',
            'inter-as',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition green',
                'address-family ipv4',
                'mdt auto-discovery vxlan inter-as',
            ]
        )
