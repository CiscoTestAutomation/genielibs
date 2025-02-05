from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_macro_auto_execute
from unittest.mock import Mock


class TestConfigureMacroAutoExecute(TestCase):

    def test_configure_macro_auto_execute(self):
        self.device = Mock()
        result = configure_macro_auto_execute(self.device, 'test_trigger', 'ACCESS_VLAN=70', ['if [[ $LINKUP == YES ]]',
 'then conf t',
 'interface $INTERFACE',
 'macro description $TRIGGER',
 'description [VOIP] PBX',
 'switchport access vlan $ACCESS_VLAN',
 'switchport mode access',
 'switchport voice vlan 1100',
 'authentication periodic',
 'authentication timer reauthenticate 50',
 'access-session host-mode multi-domain',
 'access-session closed',
 'access-session port-control auto',
 'snmp trap mac-notification change added',
 'dot1x pae authenticator',
 'dot1x timeout tx-period 10',
 'dot1x max-reauth-req 3',
 'storm-control broadcast level 1.00',
 'storm-control action trap',
 'spanning-tree portfast',
 'spanning-tree bpduguard enable',
 'service-policy type control subscriber test_dot1x',
 'exit',
 'fi'], ['if [[ $LINKUP == NO ]]',
 'then conf t',
 'default interface $INTERFACE',
 'exit',
 'fi'])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['macro auto execute test_trigger ACCESS_VLAN=70{', 'if [[ $LINKUP == YES ]]', 'then conf t', 'interface $INTERFACE', 'macro description $TRIGGER', 'description [VOIP] PBX', 'switchport access vlan $ACCESS_VLAN', 'switchport mode access', 'switchport voice vlan 1100', 'authentication periodic', 'authentication timer reauthenticate 50', 'access-session host-mode multi-domain', 'access-session closed', 'access-session port-control auto', 'snmp trap mac-notification change added', 'dot1x pae authenticator', 'dot1x timeout tx-period 10', 'dot1x max-reauth-req 3', 'storm-control broadcast level 1.00', 'storm-control action trap', 'spanning-tree portfast', 'spanning-tree bpduguard enable', 'service-policy type control subscriber test_dot1x', 'exit', 'fi', 'if [[ $LINKUP == NO ]]', 'then conf t', 'default interface $INTERFACE', 'exit', 'fi', '}'],)
        )
