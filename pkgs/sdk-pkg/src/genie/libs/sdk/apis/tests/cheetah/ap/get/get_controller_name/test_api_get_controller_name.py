import unittest
from unittest.mock import Mock

from genie.libs.parser.cheetah.show_capwap import ShowCapwapClientRcb
from genie.libs.sdk.apis.cheetah.ap.get import get_controller_name


CAPWAP_CLIENT_RCB_OUTPUT = """\
AdminState                         : ADMIN_ENABLED
OperationState                     : UP
Name                               : AP188B.4500.5EE8
SwVer                              : 17.7.1.2
HwVer                              : 1.0.0.0
MwarApMgrIp                        : 9.4.62.51
MwarName                           : vidya-ewlc-5
MwarHwVer                          : 0.0.0.0
Location                           : default location
ApMode                             : Local
ApSubMode                          : Not Configured
CAPWAP Path MTU                    : 1485
Software Initiated Reload Reason   : Controller Reload command
Active Window Size                 : 1
OOB Image Download                 : Enabled
CAPWAP UDP-Lite                    : Enabled
IP Prefer-mode                     : IPv4
AP Link DTLS Encryption            : OFF
AP TCP MSS Adjust                  : Enabled
AP TCP MSS size                    : 1250
LinkAuditing                       : disabled
AP Group Name                      : default-group
CAPWAP Disconnect Reason:
    Controller Last Sent: No value set
Cisco Trustsec Config
  AP Inline Tagging Mode            : Disabled
  AP Sgacl Enforcement              : Disabled
  AP Override Status                : Disabled
Total Flash Writes Since Boot      : 631
BLE Module Admin State              : Disabled
Hyperlocation Admin State          : Disabled
"""


class TestGetControllerName(unittest.TestCase):

    def test_get_controller_name(self):
        device = Mock()
        device.parse.return_value = ShowCapwapClientRcb(device).cli(
            output=CAPWAP_CLIENT_RCB_OUTPUT)

        result = get_controller_name(device)

        expected_output = 'vidya-ewlc-5'
        self.assertEqual(result, expected_output)
        device.parse.assert_called_once_with('show capwap client rcb')
