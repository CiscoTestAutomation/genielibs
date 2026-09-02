import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    unconfigure_mdt_data_threshold,
)


class TestUnconfigureMdtDataThreshold(unittest.TestCase):

    def test_unconfigure_mdt_data_threshold(self):
        device = Mock()

        result = unconfigure_mdt_data_threshold(
            device=device,
            vrf_name='vrf3001',
            address_family='ipv4',
            threshold=1,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition vrf3001',
                'address-family ipv4',
                'no mdt data threshold 1',
            ]
        )
