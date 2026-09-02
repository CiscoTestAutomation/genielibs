import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import configure_default_vxlan


class TestConfigureDefaultVxlan(unittest.TestCase):

    def test_configure_default_vxlan(self):
        device = Mock()

        result = configure_default_vxlan(
            device,
            'green',
            'ipv4',
            '239.1.1.1',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition green',
                'address-family ipv4',
                'mdt default vxlan  239.1.1.1',
            ]
        )
