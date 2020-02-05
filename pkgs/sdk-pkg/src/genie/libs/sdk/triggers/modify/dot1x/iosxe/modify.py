'''IOSXE Implementation for Dot1x modify triggers'''

# import ATS
from pyats import aetest

# import genie.libs
from genie.libs import conf
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify


# Which key to exclude for lldp Ops comparison
lldp_exclude = ['maker', 'counters', 'management_address']

# Which key to exclude for dot1x Ops comparison
dot1x_exclude = ['maker', 'statistics', 'session']

# Which key to exclude for fdb Ops comparison
fdb_exclude = ['maker', 'total_mac_addresses']

class TriggerModifyDot1xUserCredential(TriggerModify):
    """Modify and revert the dot1x user credential"""

    __description__ = """Modify and revert the dot1x user credential

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the end
                of the trigger execution. Used when previous timeouts have been exhausted.

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                interface: `str`
                client: `str`
                vlan: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                    OR
                    interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Dot1x Ops object to check if there is any 'auth' interface(s),
           otherwise SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the dot1x user cedential to mimatched values with DOT1x Conf object on uut
        4. Verify the status of dot1x changed from 'auth' to 'unauth' from step 3,
           Verify the peer mac-address in UUT's table is 'drop'
        5. Recover the device configurations to the one in step 2
        6. Learn Dot1x Ops again and verify it is the same as the Ops in step 1

    """        

    @aetest.test
    def save_configuration(self, uut, method, abstract):
        super().save_configuration(uut.peer, method, abstract)

    @aetest.test
    def modify_configuration(self, uut, abstract, steps):
        super().modify_configuration(uut.peer, abstract, steps)

        # shut no shut the interface on UUT to let the session restart
        for key in self.mapping.keys:
            if hasattr(uut, 'interfaces') and key['interface'] in uut.interfaces:
                intf_conf = uut.interfaces[key['interface']]
            else:
                intf_conf = abstract.conf.interface.Interface(device=uut, name=key['interface'])
            intf_conf.enabled = False
            intf_conf.build_config()
            intf_conf.build_unconfig(attributes={'enabled': None})


    @aetest.test
    def restore_configuration(self, uut, method, abstract):
        super().restore_configuration(uut.peer, method, abstract)

        # shut no shut the interface on UUT to let the session restart
        for key in self.mapping.keys:
            if hasattr(uut, 'interfaces') and key['interface'] in uut.interfaces:
                intf_conf = uut.interfaces[key['interface']]
            else:
                intf_conf = abstract.conf.interface.Interface(device=uut, name=key['interface'])
            intf_conf.enabled = False
            intf_conf.build_config()
            intf_conf.build_unconfig(attributes={'enabled': None})
            del(uut.interfaces[key['interface']])


    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.dot1x.dot1x.Dot1x':{
                                       'requirements':[['info', 'interfaces', '(?P<interface>.*)',
                                                        'clients', '(?P<client>.*)', 'status', 'authorized']],
                                       'all_keys': True,
                                       'kwargs':{'attributes':['info[interfaces][(.*)][clients][(.*)][status]',
                                                               'info[sessions]']},
                                       'exclude': dot1x_exclude},
                                    'ops.fdb.fdb.Fdb':{
                                       'requirements':[['info', 'mac_table', 'vlans', '(?P<vlan>.*)',
                                                        'mac_addresses', '(?P<client>.*)',
                                                        'interfaces', '(?P<interface>.*)', 'entry_type', 'static']],
                                       'all_keys': True,
                                       'kwargs':{'attributes':['info[mac_table][vlans][(.*)]']},
                                       'exclude': fdb_exclude + ['mac_addresses']}},
                      config_info={'conf.dot1x.Dot1x':{
                                       'requirements':[['device_attr', '{uut}', 'credentials_attr', 'wrong',
                                                        'credential_username', 'wrong'],
                                                       ['device_attr', '{uut}', 'credentials_attr', 'wrong',
                                                        'credential_pwd_type', '0'],
                                                       ['device_attr', '{uut}', 'credentials_attr', 'wrong',
                                                        'credential_secret', 'wrong'],
                                                       ['device_attr', '{uut}', 'interface_attr', '(?P<peer_intf>.*)',
                                                        'if_credentials', 'wrong']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.dot1x.dot1x.Dot1x':{
                                       'requirements':[['info', 'interfaces', '(?P<interface>.*)',
                                                        'clients', '(?P<client>.*)', 'status', 'unauthorized'],
                                                       ['info', 'sessions', 'authorized_clients', '(\d+)'],
                                                       ['info', 'sessions', 'unauthorized_clients', '(\d+)']],
                                       'kwargs':{'attributes':['info[interfaces][(.*)][clients][(.*)][status]',
                                                               'info[sessions]']},
                                       'exclude': dot1x_exclude},
                                  'ops.fdb.fdb.Fdb':{
                                       'requirements':[['info', 'mac_table', 'vlans', '(?P<vlan>.*)',
                                                        'mac_addresses', '(?P<client>.*)',
                                                        'drop', 'drop', True],
                                                       ['info', 'mac_table', 'vlans', '(?P<vlan>.*)',
                                                        'mac_addresses', '(?P<client>.*)',
                                                        'drop', 'entry_type', 'dynamic']],
                                       'kwargs':{'attributes':['info[mac_table][vlans][(.*)]']},
                                       'exclude': fdb_exclude + ['mac_addresses']}},
                      num_values={'interface': 'all'})