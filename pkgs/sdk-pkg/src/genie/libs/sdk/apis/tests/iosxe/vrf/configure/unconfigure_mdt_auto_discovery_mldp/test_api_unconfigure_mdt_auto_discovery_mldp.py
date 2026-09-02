import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    unconfigure_mdt_auto_discovery_mldp,
)


class TestUnconfigureMdtAutoDiscoveryMldp(unittest.TestCase):

    def test_unconfigure_mdt_auto_discovery_mldp(self):
        device = Mock()

        result = unconfigure_mdt_auto_discovery_mldp(
            device,
            'vrf3001',
            'ipv4',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'vrf definition vrf3001\n'
            ' address-family ipv4\n'
            ' no mdt auto-discovery mldp'
        )
