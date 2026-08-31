import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    configure_vrf_definition_stitching,
)


class TestConfigureVrfDefinitionStitching(unittest.TestCase):

    def test_configure_vrf_definition_stitching(self):
        device = Mock()

        result = configure_vrf_definition_stitching(
            device,
            'red',
            '1:100',
            'ipv6',
            '100:100',
            '1:1',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition red',
                'rd 1:100',
                'address-family ipv6',
                'route-target export 100:100',
                'route-target import 100:100',
                'route-target export 1:1 stitching',
                'route-target import 1:1 stitching',
                'exit-address-family',
            ]
        )
