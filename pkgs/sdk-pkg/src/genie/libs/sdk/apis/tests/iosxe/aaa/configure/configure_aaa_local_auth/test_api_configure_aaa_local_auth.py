import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_local_auth


class TestConfigureAaaLocalAuth(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_aaa_local_auth(self):
        result = configure_aaa_local_auth(self.device, 'MACSEC-UPLINK', 1)
        self.device.configure.assert_called_once_with([
            'aaa authentication dot1x MACSEC-UPLINK local',
            'aaa local authentication MACSEC-UPLINK authorization MACSEC-UPLINK',
            'aaa authorization network MACSEC-UPLINK local',
            'aaa authorization credential-download MACSEC-UPLINK local'
        ])
