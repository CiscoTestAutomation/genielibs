import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    configure_mdt_preference_under_vrf,
)


class TestConfigureMdtPreferenceUnderVrf(unittest.TestCase):

    def test_configure_mdt_preference_under_vrf(self):
        device = Mock()

        result = configure_mdt_preference_under_vrf(
            device,
            'vrf3001',
            'ipv4',
            'mldp',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition vrf3001',
                'address-family ipv4',
                'mdt preference mldp',
            ]
        )
