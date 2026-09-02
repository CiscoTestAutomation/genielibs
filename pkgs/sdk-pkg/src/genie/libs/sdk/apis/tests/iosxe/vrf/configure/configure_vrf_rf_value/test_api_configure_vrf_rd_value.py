import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import configure_vrf_rd_value


class TestConfigureVrfRdValue(unittest.TestCase):

    def test_configure_vrf_rd_value(self):
        device = Mock()

        result = configure_vrf_rd_value(
            device,
            'red',
            '2:100',
            'ipv4',
            'export',
            '2:10',
            'stitching',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition red',
                'rd 2:100',
                'address-family ipv4',
                'route-target export 2:10 stitching',
                'exit-address-family',
            ]
        )
