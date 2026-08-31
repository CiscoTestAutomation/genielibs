import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import configure_mdt_default


class TestConfigureMdtDefault(unittest.TestCase):

    def test_configure_mdt_default(self):
        device = Mock()

        result = configure_mdt_default(
            device,
            'green',
            'ipv4',
            '239.2.2.2',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition green',
                'address-family ipv4',
                'mdt default 239.2.2.2',
            ]
        )
