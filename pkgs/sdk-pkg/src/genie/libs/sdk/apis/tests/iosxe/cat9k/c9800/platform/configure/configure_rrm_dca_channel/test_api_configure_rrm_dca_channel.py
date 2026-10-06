import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.configure import (
    configure_rrm_dca_channel,
)
from unicon.core.errors import SubCommandFailure


class TestConfigureRrmDcaChannel(unittest.TestCase):

    def test_configure_rrm_dca_channel(self):
        device = Mock()
        device.name = 'WLC1'

        configure_rrm_dca_channel(device, ['52', '56'])

        device.configure.assert_called_once_with([
            'wireless rf-network WLC1',
            'ap dot11 5ghz rrm channel dca remove 52',
            'ap dot11 5ghz rrm channel dca remove 56',
            'ap dot11 5ghz rrm group-mode auto',
        ])

    def test_configure_rrm_dca_channel_failure(self):
        device = Mock()
        device.name = 'WLC1'
        device.configure.side_effect = SubCommandFailure(
            'configuration failed')

        with self.assertRaisesRegex(
                SubCommandFailure, 'Failed to remove RRM DCA channels'):
            configure_rrm_dca_channel(device, ['52', '56'])
