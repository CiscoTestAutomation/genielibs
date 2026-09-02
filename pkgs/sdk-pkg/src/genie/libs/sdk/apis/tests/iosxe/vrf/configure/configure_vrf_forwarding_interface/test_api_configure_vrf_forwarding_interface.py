import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    configure_vrf_forwarding_interface,
)


class TestConfigureVrfForwardingInterface(unittest.TestCase):

    def test_configure_vrf_forwarding_interface(self):
        device = Mock()

        result = configure_vrf_forwarding_interface(
            device,
            'vlan1006',
            'vrf1',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface vlan1006',
                'vrf forwarding vrf1',
            ]
        )
