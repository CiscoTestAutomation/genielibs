import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from genie.libs.parser.cheetah.show_capwap import ShowCapwapClientRcb
from genie.libs.sdk.apis.cheetah.ap.get import get_ip_address
from genie.libs.sdk.apis.cheetah.ap.verify import verify_controller_ip


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


def parse_capwap_client_rcb(device):
    return ShowCapwapClientRcb(device).cli(output=CAPWAP_CLIENT_RCB_OUTPUT)


class TestVerifyControllerIp(unittest.TestCase):

    def test_verify_controller_ip(self):
        parse = Mock(side_effect=lambda command: parse_capwap_client_rcb(
            device))
        api_get_ip_address = Mock(
            side_effect=lambda: get_ip_address(device))
        device = SimpleNamespace(
            parse=parse,
            api=SimpleNamespace(get_ip_address=api_get_ip_address))

        self.assertTrue(verify_controller_ip(device, '9.4.62.51'))
        api_get_ip_address.assert_called_once_with()
        parse.assert_called_once_with('show capwap client rcb')

    def test_verify_controller_ip_mismatch(self):
        def parse_mismatch(command):
            parsed = parse_capwap_client_rcb(device)
            parsed['mwar_ap_mgr_ip'] = '192.0.2.1'
            return parsed

        parse = Mock(side_effect=parse_mismatch)
        api_get_ip_address = Mock(
            side_effect=lambda: get_ip_address(device))
        device = SimpleNamespace(
            parse=parse,
            api=SimpleNamespace(get_ip_address=api_get_ip_address))

        self.assertFalse(verify_controller_ip(device, '9.4.62.51'))
        api_get_ip_address.assert_called_once_with()
        parse.assert_called_once_with('show capwap client rcb')
