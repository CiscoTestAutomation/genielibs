import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    unconfigure_vrf_definition_stitching,
)


class TestUnconfigureVrfDefinitionStitching(unittest.TestCase):

    def test_unconfigure_vrf_definition_stitching(self):
        device = Mock()

        result = unconfigure_vrf_definition_stitching(
            device,
            'red',
            'ipv6',
            '1:1',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition red',
                'address-family ipv6',
                'no route-target export 1:1 stitching',
                'no route-target import 1:1 stitching',
                'exit-address-family',
            ]
        )
