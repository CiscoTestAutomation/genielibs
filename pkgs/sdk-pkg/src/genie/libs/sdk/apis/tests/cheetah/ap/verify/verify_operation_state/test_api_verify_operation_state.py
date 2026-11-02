import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from genie.libs.parser.cheetah.show_capwap import ShowCapwapClientRcb
from genie.libs.sdk.apis.cheetah.ap.get import get_operation_state
from genie.libs.sdk.apis.cheetah.ap.verify import verify_operation_state


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


class TestVerifyOperationState(unittest.TestCase):

    def test_verify_operation_state(self):
        parse = Mock(side_effect=lambda command: parse_capwap_client_rcb(
            device))
        api_get_operation_state = Mock(
            side_effect=lambda: get_operation_state(device))
        device = SimpleNamespace(
            parse=parse,
            api=SimpleNamespace(get_operation_state=api_get_operation_state))

        self.assertTrue(verify_operation_state(device, 'UP'))
        api_get_operation_state.assert_called_once_with()
        parse.assert_called_once_with('show capwap client rcb')

    def test_verify_operation_state_mismatch(self):
        def parse_mismatch(command):
            parsed = parse_capwap_client_rcb(device)
            parsed['operation_state'] = 'DOWN'
            return parsed

        parse = Mock(side_effect=parse_mismatch)
        api_get_operation_state = Mock(
            side_effect=lambda: get_operation_state(device))
        device = SimpleNamespace(
            parse=parse,
            api=SimpleNamespace(get_operation_state=api_get_operation_state))

        self.assertFalse(verify_operation_state(device, 'UP'))
        api_get_operation_state.assert_called_once_with()
        parse.assert_called_once_with('show capwap client rcb')
